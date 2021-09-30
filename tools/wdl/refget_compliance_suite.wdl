version 1.0

task createRefgetComplianceReport{
    
    input {
        String server
        String json_path
    }

    command {
        refget-compliance report --server ${server} --json_path ${json_path}
    }

    output {
        File refget_compliance_report = "${json_path}"
    }

    runtime {
        docker: "ga4gh/refget-compliance-suite:1.2.6"
    }

}

workflow refgetComplianceReportWorkflow {

    input {
        String server
        String json_path
    }

    call createRefgetComplianceReport { input: server=server, json_path=json_path }

}
