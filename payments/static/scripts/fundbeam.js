$(document).ready(function() {
    $('.view-transactions').click(function(){
        var account_number = $(this).attr("data-account_number");

        if ($('#transactions_'+ account_number).html()) {
            $('#transactions_'+ account_number).toggle();
        }
        else {
            $.get('account_transactions/', {account_number: account_number}, function(data){
                $('#transactions_'+ account_number).html(data);
            });
            $('#transactions_'+ account_number).show();
        }
    });
});