{{/* vim: set filetype=mustache: */}}
{{/*
Generate secret name.
*/}}
{{- define "common.secrets.name" -}}
{{- $name := (include "common.names.fullname" .context) -}}

{{- if .defaultNameSuffix -}}
{{- $name = printf "%s-%s" $name .defaultNameSuffix | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- with .existingSecret -}}
{{- $name = . -}}
{{- end -}}

{{- printf "%s" $name -}}
{{- end -}}

{{/*
Generate secret key.
*/}}
{{- define "common.secrets.key" -}}
{{- $key := .key -}}
{{- printf "%s" $key -}}
{{- end -}}
