function doSomething() {
    let a = document.getElementById('inputA').value;
    let b = doucment.getElementById('inputB').value;
    document.getElementById('valueA').innerHTML = a;
    document.getElementById('valueB').innerHTML = b;
    document.getElementById('valudC').innerHTML = Number(a) + Number(b);
}