
const paymentForm = document.getElementById('paymentForm');
paymentForm.addEventListener("submit", payWithPaystack, false);
function payWithPaystack(e) {
  
  e.preventDefault();
  let handler = PaystackPop.setup({
    key: 'pk_test_1dbb7c8961b4665509e687266bfbd2e1116ef793', // Replace with your public key
    email: document.getElementById("email").value,
    amount: document.getElementById("amount").value * 100,
    ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
    // label: "Optional string that replaces customer email"
    onClose: function(){
      alert('Window closed.');
    },
    callback: function(response){
      let balance = document.getElementById('balance').textContent;
      let amount = document.getElementById("amount").value;
      const sum = parseInt(balance) + parseInt(amount);
      console.log(sum);
      document.getElementById('balance').textContent= sum;
      // console.log(balance);

      let message = 'Payment complete! Reference: ' + response.reference;
      alert(message);
      $.ajax({
        type: "POST",
        url: "/fund_account_check",
        data: response.reference,
        contentType: "application/json",
        dataType: 'json' 
      });
    }
    
  });
  
  handler.openIframe();
}

function transfer(e){
  e.preventDefault();
  
}