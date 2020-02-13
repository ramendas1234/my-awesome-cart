  if(localStorage.getItem('cart') == null){
var cart = {};
}
else
{
cart = JSON.parse(localStorage.getItem('cart'));
updateCart(cart);
}
$('.cart').click(function(){
console.log('clicked');
var idstr = this.id.toString();
// console.log(idstr);
if (cart[idstr] !=undefined){
cart[idstr] = cart[idstr] + 1;
}
else
{
cart[idstr] = 1;
}
// console.log(cart);
updateCart(cart);
localStorage.setItem('cart', JSON.stringify(cart));

});
$('#popcart').popover();
document.getElementById("popcart").setAttribute('data-content', '<h5>Cart for your items in my shopping cart</h5>');

//Add Popover to cart
$('#popcart').popover();
updatePopover(cart);
function updatePopover(cart)
{
    
    var popStr = "";
    popStr = popStr + "<h5> Cart for your items in my shopping cart </h5><div class='mx-2 my-2'>";
    var i = 1;
    for (var item in cart){
        popStr = popStr + "<b>" + i + "</b>. ";
        popStr = popStr + document.getElementById('name' + item).innerHTML.slice(0, 19) + "... Qty: " + cart[item] + '<br>';
        i = i+1;
    }
    popStr = popStr + "</div>" 
    popStr = popStr + "<a href='/shop/checkout'><button class='btn btn-primary' id ='checkout'>Checkout</button></a> <button class='btn btn-primary' onclick='clearCart()' id ='clearCart'>Clear Cart</button>     "
    document.getElementById('popcart').setAttribute('data-content', popStr);
    $('#popcart').popover('show');
}


function clearCart(){
  cart = JSON.parse(localStorage.getItem('cart'));
  for(var item in cart){
      document.getElementById('div'+ item).innerHTML = '<button id="'+item+'" class="btn btn-primary cart">Add To Cart</button>';
      localStorage.clear();
      cart = {};
      updateCart(cart);
  }
}


function updateCart(cart) {
  var sum = 0 ;
    for (var item in cart) {
      sum += cart[item] ;
        document.getElementById('div' + item).innerHTML = "<button id='minus" + item + "' class='btn btn-primary minus'>-</button> <span id='val" + item + "''>" + cart[item] + "</span> <button id='plus" + item + "' class='btn btn-primary plus'> + </button>";
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    // document.getElementById('cart').innerHTML = Object.keys(cart).length;
    document.getElementById('cart').innerHTML = sum;
    
    console.log(cart);
    updatePopover(cart);
}
// IF Plus or Minus Button is clicked Change Cart
$(document).on('click','button.minus', function(){
  a = this.id.slice(7, );
  cart['pr' + a] = cart['pr' + a] - 1;
  cart['pr' + a] = Math.max(0, cart['pr' + a]);
  if(cart['pr' + a] == 0){
    delete cart['pr' + a];
    $('#divpr'+a).html('<button id="pr'+a+'" class="btn btn-primary cart">Add To Cart</button>');
  }
  //console.log(cart['pr' + a]);
    // document.getElementById('valpr' + a).innerHTML = cart['pr' + a];
    updateCart(cart);
});
$(document).on('click','button.plus', function(){
  a = this.id.slice(6, );
  cart['pr' + a] = cart['pr' + a] + 1;
  cart['pr' + a] = Math.max(0, cart['pr' + a]);
    // document.getElementById('valpr' + a).innerHTML = cart['pr' + a];
    updateCart(cart);
});