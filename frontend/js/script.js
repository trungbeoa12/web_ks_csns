document.getElementById("surveyForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Ngăn chặn load lại trang khi submit

    // Thu thập dữ liệu từ các ô checkbox
    let csvc_values = [];
    document.querySelectorAll('input[name="csvc"]:checked').forEach((el) => {
        csvc_values.push(el.value);
    });

    let csqd_values = [];
    document.querySelectorAll('input[name="csqd"]:checked').forEach((el) => {
        csqd_values.push(el.value);
    });

    // Thu thập dữ liệu từ ô nhập ý kiến khác
    let csvc_khac = document.querySelector('textarea[name="csvc_khac"]').value;
    let csqd_khac = document.querySelector('textarea[name="csqd_khac"]').value;

    // Định dạng dữ liệu gửi về backend
    let surveyData = {
        csvc: csvc_values,
        csvc_khac: csvc_khac,
        csqd: csqd_values,
        csqd_khac: csqd_khac
    };

    console.log("Dữ liệu gửi đi:", surveyData); // Debug dữ liệu trước khi gửi

    // Gửi dữ liệu đến backend bằng Fetch API
    try {
        let response = await fetch("http://127.0.0.1:8000/submit_survey", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(surveyData)
        });

        if (response.ok) {
            alert("Gửi khảo sát thành công!");
        } else {
            alert("Có lỗi xảy ra khi gửi khảo sát.");
        }
    } catch (error) {
        console.error("Lỗi kết nối:", error);
        alert("Không thể kết nối đến server.");
    }
});

