setTimeout(function () {
    $('.message').fadeOut('slow');
}, 4000);

function getLikedProducts(item_id){
    $('#heart-icon-'+item_id).each(function () {
        url = $(this).attr('data-url')

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                $('#count-likes').html(response.quantity)
                if (response.status == 'success')
                    swal(response.status, response.message, 'success')
                else if (response.status == 'error')
                    swal(response.status, response.message, 'error')
                else if (response.status == 'warning')
                    swal(response.status, response.message, 'warning')
            }
        })
    })
}

function deleteLikedItem(item_id) {
    $('#delete-liked-item-'+item_id).each(function () {

        url = $(this).attr('data-url')
        liked_product_id = $(this).attr('data-id')

        console.log(liked_product_id)

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == 'success') {
                    $('#count-likes').html(response.quantity)
                    removeLikedItem(liked_product_id);
                    swal(response.status, response.message, 'success')
                } else if (response.status == 'error')
                    swal(response.status, response.message, 'error')

                if (response.quantity == 0)
                    emptyLikedItems();
            }
        })
    })
}

function removeLikedItem(liked_product_id){
    document.getElementById('single-liked-item-'+liked_product_id).remove()
}

function emptyLikedItems(){
    document.getElementById('empty-liked-items-message').style.display = 'block';
}

function confirmAlertToChange(checkbox, text_alert){
    checkbox = document.querySelector('#id_'+checkbox).checked;
    if (!(checkbox)) {
        confirm_alert = confirm(text_alert)
        return confirm_alert
    }
}
