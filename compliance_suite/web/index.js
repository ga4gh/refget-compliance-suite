function load() {
    $.getJSON("temp_result.json", function (data) {
        var text_report = "";
        var num_reports = data.length;
        $.each(data, function (index, report) {
            console.log(report)
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
                    text_report += "<p class='text-success'>" + result['name'] + ": " +  "pass</p>"
                }
                else{
                    text_report += "<h4>" + result['name'] + "</h4>"
                }
                text_report += "<p>--->" + result['text'] + "</p>&nbsp";
            });
        });

        $("#text").html(text_report)
    });
}
