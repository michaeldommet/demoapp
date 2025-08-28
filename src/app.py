from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# --- OpenTelemetry Configuration ---
# 1. Set up TracerProvider
provider = TracerProvider()
trace.set_tracer_provider(provider)

# 2. Set up OTLP Exporter
otlp_exporter = OTLPSpanExporter(
    # optional: configure OTLP exporter endpoint
    # endpoint="http://localhost:4317"
)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

import os

app = Flask(__name__)

# --- Database Configuration ---
db_user = os.environ.get('MYSQL_USER', 'root')
db_password = os.environ.get('MYSQL_PASSWORD', 'password')
db_host = os.environ.get('MYSQL_SERVER', 'localhost')
db_name = os.environ.get('MYSQL_DATABASE', 'appdb')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 3. Instrument Flask and SQLAlchemy
FlaskInstrumentor().instrument_app(app)
with app.app_context():
    SQLAlchemyInstrumentor().instrument(engine=db.engine)

tracer = trace.get_tracer(__name__)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@app.route('/')
def index():
    # Show all todos
    todo_list = Todo.query.all()
    return render_template('index.html', todos=todo_list)

@app.route("/add", methods=["POST"])
def add():
    with tracer.start_as_current_span("add_item"):
        # Add new item
        title = request.form.get("title")
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # Update item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Delete item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
