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
        docker: "yashpuligundla/refget-compliance-suite:1.1"
    }

}

workflow refgetComplianceReportWorkflow {

    input {
        String server
        String json_path
    }

    call createRefgetComplianceReport { input: server=server, json_path=json_path }

}
