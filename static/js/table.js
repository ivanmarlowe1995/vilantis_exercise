var FieldCount = 1;
var x = FieldCount;
var tableMode;
var dynamicColumnName;
var MaxInputs = 4; //maximum input boxes allowed

function passSearchSize(size){
            x = size;
            FieldCount = size;
        }

function genDynamicColName(tableName){
    tableMode = tableName;
    if(tableMode == 'country_relation_raw'){
        dynamicColumnName = ''
        + '        <option value="id">id</option>'
        + '        <option value="allow_pirates_to_pirates">allow_pirates_to_pirates</option>'
        + '        <option value="description">description</option>'
        + '        <option value="min_rep_level_to_occur">min_rep_level_to_occur</option>'
        + '        <option value="name">name</option>'
        + '        <option value="random">random</option>'
        + '        <option value="rep_change">rep_change</option>'
        + '        <option value="stage">stage</option>'
        + '        <option value="date_created">date_created</option>'
    }
    else {
        dynamicColumnName = ''
        + '        <option value="country_id">country_id</option>'
        + '        <option value="country_a">country_a</option>'
        + '        <option value="country_b">country_b</option>'
        + '        <option value="date_updated">date_updated</option>'
        + '        <option value="relationship_score">relationship_score</option>'
    }
}

$(document).ready(function() {
        var InputsWrapper   = $("#InputsWrapper"); //Input boxes wrapper ID
        var AddButton       = $("#AddFilter"); //Add button ID

        $(AddButton).click(function (e)  //on add input button click
        {

            if(x < MaxInputs) //max input box allowed
            {
                FieldCount++; //text box added increment
                //add input box

                newSearchVar = ''
                                + '<div class="input-group row mt-4">'
                                + '    <div class="input-group">'
                                    + '    <div class="col-sm-6">'
                                    + '        <input class="form-control" type="text" placeholder="Enter column value"  name="field_'+ FieldCount +'" id="field_'+ FieldCount +'" />'
                                    + '    </div>'
                                    /*start of expression select*/
                                    + '    <select class="form-select" name="select_expr_'+ FieldCount +'" id="select_expr_'+ FieldCount +'">'
                                    + '        <option value="=">=</option>'
                                    + '        <option value="in">in</option>'
                                    + '        <option value="like">like</option>'
                                    + '        <option value=">=">>=</option>'
                                    + '        <option value="<="><=</option>'
                                    + '        <option value=">">></option>'
                                    + '        <option value="<"><</option>'
                                    + '    </select>'
                                    /*end of expression select*/
                                    /*start of column select*/
                                    + '    <select class="form-select" name="select_col_'+ FieldCount +'" id="select_expr_'+ FieldCount +'">'
                                    /*start of dynamic column select*/
                                    + ''
                                    + dynamicColumnName +
                                    + ''
                                    /*end of dynamic column select*/
                                    + '    </select>'
                                    /*end of column select*/
                                    + '    <a href="#" class="btn btn-danger removeclass">×</a>'
                                + '    </div>'
                                + '</div>'

                $(InputsWrapper).append(newSearchVar);
                x++; //text box increment
            }
        return false;
        });

        $("body").on("click",".removeclass", function(e){ //user click on remove text
                if( x > 1 ) {

                        $(this).parent('div').parent('div').remove(); //remove text box
                        x--; //decrement textbox
                        FieldCount--;

                        console.log('FieldCountDelete:' + FieldCount)
                        console.log('XDelete:'+x)
                }
        return false;
        })

        $('#submit').click(function(){
                   $.ajax({
                        url:"/postskill",
                        method:"POST",
                        data:$('#add_skills').serialize(),
                        success:function(data)
                        {  alert(data)
                             $('#resultbox').html(data);
                             $('#add_skills')[0].reset();
                        }
                   });
              });
        });