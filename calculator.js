document.addEventListener("keydown", function (event) {
    const key = event.key;
    if (key == "Enter") {
        calculateResult();
    } else if (key == "Escape") {
        clearDisplay();
    }
});


let expr = '';

function appendToDisplay(value) {
    check();
    expr += value;
    document.getElementById('display').value = expr;
    check();
}
    
function clearDisplay() {
    check();
    expr = '';
    document.getElementById('display').value = '';
    document.getElementById('display2').value = '';
    check();
}

function formatNumber(number) {
    if (Number.isInteger(number)) {
        return number; // If it is an integer, return an integer directly

    } else {
        return parseFloat(number.toFixed(6)); // If it is a decimal, keep 6 decimal places and return
    }
}

function delToDisplay() {
    check();
    expr = expr.slice(0, -1);
    document.getElementById('display').value = expr;
    check();
}

function factorial(n) {
    if (n === 0 || n === 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

function calculateResult() {
    check();
    try {
        expr = expr.replace(/lg/g, 'Math.log10').replace(/ln/g, 'Math.log').replace(/sqrt/g, 'Math.sqrt').replace(/sin/g, 'Math.sin').replace(/\^/g, '**').replace(/cos/g, 'Math.cos').replace(/tan/g, 'Math.tan').replace(/e/g, 'Math.E').replace(/pi/g, 'Math.PI').replace(/abs/g, 'Math.abs').replace(/(\d+)!/g, 'factorial($1)');
        expr = eval(expr);
        expr = formatNumber(expr);
        if (!/[0-9\.]/.test(String(expr))) expr = 'error';
        document.getElementById('display2').value = expr;
        check();

        expression = expr;
        result = document.getElementById('display2').value

        const xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://localhost:5000/post_history', true);
        xhr.setRequestHeader('Content-type', 'application/json');

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                console.log(xhr.responseText);
            }
        };

        const data = {
        expression: expression,
        result: result
        };

        xhr.send(JSON.stringify(data));

    } catch (error) {
        document.getElementById('display').value = '';
        document.getElementById('display2').value = 'error';
    }
}


function check() {
    expr = document.getElementById('display').value;
}

function send_clear(){
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:5000/send_clear', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.send();
}

function get_message(){
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://localhost:5000/get_calculation_data', true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
            Data = JSON.parse(xhr.responseText);
            array = Data['data'];
            let string="";
            for(let i=0;i<array.length;i++){
                string +=array[i][0]+" = "+array[i][1]+"\n";
            }
            document.getElementById('display').value = string;
        } else {
            console.error('获取数据出错: ' + xhr.status);
        }
      }
    };
    xhr.send();
}
