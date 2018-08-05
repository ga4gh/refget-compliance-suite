function load() {
    $.getJSON("temp_result.json", function (data) {
        var text_report = "";
        var num_reports = data.length;
        var num_tests = data[0]["test_results"].length
        console.log(data)
        $.each(data, function (index, report) {
            text_report += "<h3>Server: " + report['server'] + "</h3>"
            text_report += "<p>Total tests: " + report["total_tests"] + "</p>"
            text_report += "<p>Total tests passed: " + report["total_tests_passed"] + "</p>"
            text_report += "<p>Total tests failed: " + report["total_tests_failed"] + "</p>"
            text_report += "<p>Total tests skipped: " + report["total_tests_skipped"] + "</p>"
            text_report += "<p>Total warnings generated: " + report["total_warnings"] + "</p>"
            text_report += "&nbsp<p><b>Test result reports</b></h3>"

            $.each(report['test_results'], function (index, result){
                console.log(result)
                if(result["result"] == 1){
                    text_report += "<p class='text-success'>" + result['name'] + ": " +  "PASSED</p>"
                }
                else if (result["result"] == 0 && result["warning"] == true){
                    text_report += "<p class='text-warning'>" + result['name'] + ": " +  "SKIPPED | WARNING</p>"
                }
                else if (result["result"] == 0 && result["warning"] == false){
                    text_report += "<p class='text-info'>" + result['name'] + ": " +  "SKIPPED</p>"
                }
                else {
                    text_report += "<p class='text-danger'>" + result['name'] + ": " +  "FAILED | WARNING</p>"
                }
                text_report += "<p>--->" + result['text'] + "</p>&nbsp";
            });

            text_report += "-----------------------------------------------------------------"
        });

        $("#text").html(text_report)

        var t_head = "<tr><th>Test Cases</th>"
        for(i=0; i<num_reports; i++){
            t_head += "<th>" + data[i].server + "</th>"
        }
        t_head += "</tr>"
        $("#compliance_matrix").find("thead").html(t_head)

        var t_body = ""
        for(i=0; i<num_tests; i++){
            t_body += "<tr><td>" + data[0]["test_results"][i]["name"] + "</td>"
            for(j=0; j<num_reports; j++){
                var test = data[j]["test_results"][i]

                if (test["result"] == 1){
                    t_body += "<td class='text-success'>PASSED</td>"
                }
                else if(test["result"] == 0 && test["warning"] == true){
                    t_body += "<td class='text-warning'>SKIPPED | WARNING</td>"
                }
                else if(test["result"] == 0 && test["warning"] == false){
                    t_body += "<td class='text-info'>SKIPPED</td>";
                }
                else{
                    t_body += "<td class='text-danger'>FAILED | WARNING</td>"
                }
            }
            t_body += "</tr>"
            console.log(t_body)
        }
        $("#compliance_matrix").find("tbody").html(t_body)



    });



}
