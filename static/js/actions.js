(function($){
    $(document).ready(function() {

        // Привязка датапикера к полю ввода
        $('.datepicker-history').datepicker({
            format: 'dd.mm.yyyy',
            endDate: '+0d',
            language: 'ru',
        });

    });
})(jQuery);

