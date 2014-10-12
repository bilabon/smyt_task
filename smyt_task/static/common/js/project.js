function main(model) {
    // Create table with all users
    $("#dynamictable").css("visibility", "hidden");
    $('table#main').remove();
    $('#dynamictable').append('<table id="main"></table>');
    table = $('#dynamictable').children();
    $.ajax({
        type: 'GET',
        url: '/api/v1/' + model + '/',
        data: {},
        complete: function (r) {
            value = jQuery.parseJSON(r.responseText);
            if (!jQuery.isEmptyObject(value[model])){
                table.append(draw_head_table(value));
                each_value(value);
                $('.update.datepicker').datepicker("destroy");
                $('.update.datepicker').datepicker({
                    dateFormat: 'yy-mm-dd'
                });
                $('input.update').change(function () {
                    $this = $(this);

                    var pk = $this.attr('data-pk');
                    var key = $this.attr('data-key');
                    var value = $this.val();

                    console.log('main() pk: ' + pk);
                    console.log('main() key: ' + key);
                    console.log('main() value: ' + value);

                    validate($(this));

                    if ($this.attr('data-error') == 'false') {
                        // if not error then update input
                        $this.effect("highlight", {
                            color: "green"
                        }, 500);
                        var data = {};
                        data[key] = value;
                        $.ajax({
                            type: 'POST',
                            url: '/api/v1/' + model + '/' + pk + '/',
                            data: data,
                            complete: function (r) {
                                value = jQuery.parseJSON(r.responseText);
                                if (value['success'] === false) {
                                    console.log('main() Some error: ' + value['message']);
                                }
                            }
                        });
                    }

                });
            $("#dynamictable").css("visibility", "visible");
            }
        }
    });
}


function create(model) {
    // Here we add ability to create user
    $("#add_record").css("visibility", "hidden");
    $('table#create').remove();
    $('#add_form').remove();
    $('#add_record').append('<form id="add_form" method="post" action="' + '/api/v1/' + model + '/' + '" ><table id="create"></table></form>');
    var add_record_table = $('#add_record').children().children();
    add_record_table.append('<tr><td>Add new</td></tr>');

    //Getting names of User fields from api '/api/v1/model/fields/'
    $.ajax({
        type: 'GET',
        url: '/api/v1/' + model + '/fields/',
        data: {},
        complete: function (r) {
            create_values = jQuery.parseJSON(r.responseText);
            $.each(create_values, function (id, field) {
                input = draw_input(pk = '', key = field, value = '', add_class = 'create', str = '');
                add_record_table.append('<tr><td>' + field + '&nbsp;' + input + '</td></tr>');
                $('.create.datepicker').datepicker("destroy");
                $('.create.datepicker').datepicker({
                    dateFormat: 'yy-mm-dd'
                });
            });

            add_record_table.append('<tr><td><input type="button" value="Create"></td></tr>');
            $('input.create').change(function () {
                validate($(this));
            });

            $("input[type='button']").click(function () {
                var error = false;
                $.each(create_values, function (id, field) {
                    if (validate($("input.create[name='" + field + "']")[0]) === 'true' & error === false) {
                        error = true;
                    }
                });
                if (error === false) {
                    send_form(model);
                }
            });
        $("#add_record").css("visibility", "visible");
        }
    });
}


var each_value = function (value) {
    // Drawing table rows
    $.each(value[model], function (key, value) {

        $.each(value, function (key, value) {
            if (key == 'pk') {
                pk = value;
                row = '<tr><td>';
                row += draw_input(pk, key, value, add_class = 'update', str = 'readonly="readonly"');
                row += '</td>';
            }
            if (key == 'fields') {
                $.each(value, function (key, value) {
                    row += '<td>';
                    row += draw_input(pk, key, value, add_class = 'update', str = '');
                    row += '</td>';

                });
                row += '</tr>';
                table.append(row);
            }


        });
    });
};


var draw_input = function (pk, key, value, add_class, str) {
    // Draw input
    if (key == 'date_joined') {
        add_class += ' datepicker';
        str += 'readonly="readonly"';
    }
    td = '<input type="text" ' + str + 'class="' + add_class + '" name="' + key + '" maxlength="200" data-pk="' + pk + '" data-key="' + key + '" value="' + value + '" data-error="false">';
    return td;
};


var draw_head_table = function (value) {
    // Drawing names of table columns
    row = '<tr><td>ID</td>';
    $.each(value[model][0]['fields'], function (key, value) {
        row += '<td>' + key + '</td>';
    });
    row += '</tr>';
    return row;
};


function validate(th) {
    // Fields validation
    $this = $(th);
    var val = $this.val();
    var status = '';

    if ($this.attr('data-key') == 'paycheck' || $this.attr('data-key') == 'spots') {

        if ($.isNumeric(val) === true) {
            console.log('validate() OK');
            status = 'false';
            error('white', status);

        } else {
            console.log('validate() Error');
            status = 'true';
            error('red', status);
        }
    } else {
        if (val === '') {
            console.log('validate() Error');
            status = 'true';
            error('red', status);
        } else {
            console.log('validate() OK');
            status = 'false';
            error('white', status);
        }
    }
    return status;
}


function send_form(model) {
    var msg = $('#add_form').serialize();

    var formURL = $('#add_form').attr("action");
    console.log('send_form() msg: ' + msg + 'formURL: ' + formURL);
    $.ajax({
        type: 'POST',
        url: formURL,
        data: msg,
        success: function (data) {
            console.log('send_form() Answer: ' + data);
            main(model = model);
        },
        error: function (xhr, str) {
            console.log('send_form() Some error: ' + xhr.responseCode);
        }
    });

}


function error(bgcolor, status) {
    // Function for change color and status if error
    $this.css("background-color", bgcolor);
    $this.attr('data-error', status);
}
