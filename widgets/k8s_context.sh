#!/usr/bin/env bash
# Widget: Kubernetes context and namespace
ctx=$(kubectl config current-context 2>/dev/null)
[ -z "$ctx" ] && exit 0
ns=$(kubectl config view --minify -o jsonpath='{.contexts[0].context.namespace}' 2>/dev/null)
[ -n "$ns" ] && echo "⎈ ${ctx}/${ns}" || echo "⎈ ${ctx}"
