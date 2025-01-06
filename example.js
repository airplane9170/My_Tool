// document.getElementById("submitbtn0").addEventListener("click", async () => {
//     console.log("Hi~")
//     const selectValue = document.getElementById('select_stockname').value;
//     const fibHighValue = document.getElementById('pivothigh_input').value;
    
//     const response = await fetch("/plz_do", {
//         method: 'POST',
//         headers: {
//         'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//         select_value: selectValue,
//         fib_high: fibHighValue,
//         }),
//     })
// });

// 버튼 클릭 이벤트 설정
document.getElementById("submitbtn0").addEventListener("click", function () {
    // select 요소의 값 가져오기
    const selectValue = document.getElementById("select_stockname").value;

    // input 요소의 값 가져오기
    const pivotHighValue = document.getElementById("pivothigh_input").value;

    // 값 출력
    alert("선택된 값: " + selectValue + "\n입력된 값: " + pivotHighValue);
    console.log("선택된 값:", selectValue);
    console.log("입력된 값:", pivotHighValue);

    // $.ajax({
    //     url : "/plz_do",
    //     type : "POST",
    //     data: JSON.stringify({ stock_name: selectValue, state: pivotHighValue}),
    //     success: function (response) {
    //     console.log("서버 응답:", response); // 서버 응답 출력
    //     },
    //     error: function (xhr, status, error) {
    //         console.error("요청 실패:", error); // 오류 처리
    //     }

    // })

});
