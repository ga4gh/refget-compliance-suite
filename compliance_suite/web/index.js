function load() {
    $.getJSON("temp_result.json", function (data) {
        var text_report = "<h3>Compliance Report Text</h3>";
        var num_reports = data.length;
        //var num_tests = data[0].test_results.length;
        //console.log(data);
        text_report += "<h4>Server: " + "</h4>" ;
        text_report += "<p>schema_name: " + data.schema_name + "</p>";
        text_report += "<p>schema_version: " + data.schema_version + "</p>";
        text_report += "<p>testbed_name: " + data.testbed_name + "</p>";
        text_report += "<p>testbed_version: " + data.testbed_version + "</p>";
        text_report += "<p>testbed_description: " + data.testbed_description + "</p>";
        text_report += "<p>platform_name: " + data.platform_name + "</p>";
        text_report += "<p>platform_description: " + data.platform_description + "</p>";
        text_report += "<p>input_parameters: " + data.input_parameters + "</p>";
        text_report += "<p>start_time: " + data.start_time + "</p>";
        text_report += "<p>end_time: " + data.end_time + "</p>";
        text_report += "<p>status: " + data.status + "</p>";
        text_report += "<h3>Test result reports</h3>";
        $.each(data.phases, function (index, phase) {
            text_report += "<h4>Phase: " + phase.phase_name + "</h4>";
            text_report += "<p>Phase description: " + phase.phase_description + "</p>";
            text_report += "<p>Start time: " + phase.start_time + "</p>";
            text_report += "<p>End time: " + phase.end_time + "</p>";
            text_report += "<p>Status: " + phase.status + "</p>";
            text_report += "<p>Summary:" + 
            "</br>unknown: " + phase.summary.unknown +
            "</br>passed: " + phase.summary.passed + 
            "</br>warned: " + phase.summary.warned + 
            "</br>failed: " + phase.summary.failed + 
            "</br>skipped: " + phase.summary.skipped + "</p>";
            //text_report += "<h3>Test result reports</h3>";
            
            $.each(phase.tests, function (index, test){ 
                console.log(test);
                if(test.status == "PASS"){
                    text_report += "<p class='text-success'>" + test.test_name + ": " +  "PASSED</p>";
                }
                else if (test.status == "SKIP"){
                    text_report += "<p class='text-info'>" + test.test_name + ": " +  "SKIPPED</p>";
                }
                //else if (test.status == 0 && result.warning == false){
                //    text_report += "<p class='text-warning'>" + result.name + ": " +  "SKIPPED</p>";
                //}
                else {
                    text_report += "<p class='text-danger'>" + test.test_name + ": " +  "FAILED | WARNING</p>";
                }
                text_report += "<p>--->" + test.test_description + "</p>&nbsp;";
                if(test.cases.length > 1){
                    var table = '<table style="margin-left:20px" class="table"><thead><tr><th>API</th><th>Result</th></tr></thead><tbody>';

                    $.each(test.cases, function(index, test_case){
                        if(index > 0){
                            var row = '<tr><td>';
                            row += test_case.log_messages + '</td>';
                            if(test_case.status == "PASS"){
                                row += '<td class="text-success">PASSED</td></tr>';
                            }
                            else if(test_case.status == "SKIP") {
                                row += '<td>SKIPPED</td></tr>';
                            }
                            //else if (test_case.result == 0 && ! test_case.result.warning) {
                            //    row += '<td>SKIPPED</td></tr>';
                            //}
                            else{
                                row += '<td class="text-warning">FAILED</td></tr>';
                            }
                            table += row;
                        }
                    })
                    table += '</tbody></table>';
                    text_report += table;
                }
            });

            text_report += "-----------------------------------------------------------------";
        });

        $("#text").html(text_report);

        var t_head = "<tr><th>Test Cases</th>";
        for(i=0; i<num_reports; i++){
            t_head += "<th>" + data[i].server + "</th>";
        }
        t_head += "</tr>";
        $("#compliance_matrix").find("thead").html(t_head);

        var t_body = "";
        for(i=0; i<num_tests; i++) {
            t_body += "<tr><td>" + data[0]["test_results"][i]["name"] + "</td>";
            for(j=0; j<num_reports; j++){
                var test = data[j]["test_results"][i];

                if (test.result == 1){
                    t_body += "<td class='text-success'>PASSED</td>";
                }
                else if(test.result == 0 && test.warning){
                    t_body += "<td class='text-warning'>SKIPPED | WARNING</td>";
                }
                else if(test.result == 0 && ! test.warning){
                    t_body += "<td class='text-info'>SKIPPED</td>";
                }
                else{
                    t_body += "<td class='text-danger'>FAILED | WARNING</td>";
                }
            }
            t_body += "</tr>";
            console.log(t_body);
        }
        $("#compliance_matrix").find("tbody").html(t_body);

        var json_container = $('#json');
        json_container
            .jsonPresenter('destroy')
            .jsonPresenter({
                    json: data, // JSON objects here
                });

        var data_str = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
        $('<a href="data:' + data_str + '" download="data.json"><button style="margin:10px; width:100%" class="btn"><i class="fa fa-download"></i> Download</button></a>').prependTo('#json');        
    });




}
