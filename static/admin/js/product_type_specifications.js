(function($){
    $(document).ready(function(){
        // Add class for choice field ProductType
        $('#id_product_type').addClass('product-type-specification');
        // Function to update the list of specifications when ProductType changes
        $('.product-type-specification').change(function(){
            let productTypeId = $(this).val();
            if (productTypeId) {
                let specificationsDropdowns = $('#spec-group').find('.field-specification select');

                $.ajax({
                    url: '/get_specifications/' + productTypeId + '/',
                    success: function (data) {
                        // Сохраняем текущее выбранное значение для каждого specificationsDropdown
                        specificationsDropdowns.each(function (index, dropdown) {
                            let currentValue = $(dropdown).val();

                            // Очищаем предыдущие значения и добавляем новые
                            $(dropdown).empty().append($('<option>', {
                                value: '',  // Пустое значение
                                text: '---------'
                            }));

                            $.each(data, function (index, item) {
                                $(dropdown).append($('<option>', {
                                    value: item.id,
                                    text: item.name,
                                    selected: item.id == currentValue  // Устанавливаем selected, если значение совпадает с предыдущим
                                }));
                            });
                        });
                    }
                });
            }
        });
    });
})(django.jQuery);
