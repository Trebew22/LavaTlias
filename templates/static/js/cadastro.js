function add_veiculo() {
    var container = document.getElementById('veiculo'); 

    html = '<br>\
            <div class="row"> <div class="col-md"> <input name="modelo" type="text" class="form-control" placeholder="Modelo..."> </div> <div class="col-md"> <input name="marca" type="text" class="form-control" placeholder="Marca..."></div> <div class="col-md"><input name="ano" min="1900" max="2050" type="number" class="form-control" placeholder="Ano..."></div> </div> <br>\
            <div class="row"> <div class="col-md"><input name="placa" maxlength="9" type="text" class="form-control" placeholder="Placa..."></div> <div class="col-md"><label>Insira imagem do veiculo</label><input name="imagem" type="file" class="form-control-file"></div> </div> <hr>'

    container.innerHTML += html
}

function exibir_form(n){
    att = document.getElementById('form_att')
    add = document.getElementById('form_add')

    if(n == 1){
        add.style.display = 'block'
        att.style.display = 'none'
    }
    else if(n == 2){
        add.style.display = 'none'
        att.style.display = 'block'
    }
}

function dados_cliente(){

    cliente = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value

    id_cliente = cliente.value

    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/att/", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        
        document.getElementById('form_att_cliente').style.display = 'block'

        nome = document.getElementById('nome')
        nome.value = data['cliente']['nome']

        email = document.getElementById('email')
        email.value = data['cliente']['email']

        cpf = document.getElementById('cpf')
        cpf.value = data['cliente']['cpf']

        telefone = document.getElementById('telefone')
        telefone.value = data['cliente']['telefone']

        div_veiculo = document.getElementById('form-att-veiculos')
        div_veiculo.innerHTML = '<hr><h1>Veiculos:</h1>'

        for(i=0; i < data['veiculos'].length; i++) {

            console.log(data)
  
            div_veiculo.innerHTML += '<br><form action="/att_veiculo/'+ data['veiculos'][i]['id'] +'" method="POST" id="form-att-veiculos">\
            <div class="row">\
                <div class="col-md">\
                    <input value="'+ data['veiculos'][i]['veiculo']['modelo'] +'" name="modelo" type="text" class="form-control" placeholder="Modelo..."> \
                </div>\
                <div class="col-md">\
                <input value="'+ data['veiculos'][i]['veiculo']['marca'] +'" name="marca" type="text" class="form-control" placeholder="Marca...">\
                </div>\
                <div class="col-md">\
                <input value="'+ data['veiculos'][i]['veiculo']['ano'] +'" name="ano" min="1900" max="2050" type="number" class="form-control" placeholder="Ano...">\
                </div>\
            </div><br>\
            <div class="row">\
                <div class="col-md">\
                <input value="'+ data['veiculos'][i]['veiculo']['placa'] +'" name="placa" maxlength="9" type="text" class="form-control" placeholder="Placa...">\
                </div>\
                <div class="col-md">\
                <button type="submit" class="btn btn-success">Salvar</button>\
                </div>\
                <div class="col-md">\
                <a href="/excluir_veiculo/'+ data['veiculos'][i]['id'] +'" type="submit" class="btn btn-danger">Excluir</a>\
                </div>\
            </div>\
            </form>'
        } // #TODO: remover bug

    })
}