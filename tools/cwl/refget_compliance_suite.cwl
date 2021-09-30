#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand:
hints:
  DockerRequirement:
    dockerPull: ga4gh/refget-compliance-suite:1.2.6
inputs:
  no_web:
    type: boolean
    inputBinding:
      position: 1
      prefix: --no-web
  server:
    type: string
    inputBinding:
      position: 2
      prefix: --server
  json_path:
    type: string
    inputBinding:
      position: 3
      prefix: --json_path
  
outputs:
  refget-compliance-report:
    type: File
    outputBinding:
      glob: $(inputs.json_path)