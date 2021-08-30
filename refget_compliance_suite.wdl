version 1.0

task createRefgetComplianceReport{
    
    input {
        String server
        String output_json_path
    }

    command {
        refget-compliance report --server ${server} --json_path ${output_json_path}
    }

    output {
        File bamstats_report = "${output_json_path}"
    }

    runtime {
        docker: "ga4gh/refget-compliance-suite:1.2.6"
    }

}

workflow refgetComplianceReportWorkflow {

    input {
        String server
        String output_json_path
    }

    call createRefgetComplianceReport { input: server=server, output_json_path=output_json_path }

}
