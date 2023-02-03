function add_veiculo() {
    var container = document.getElementById('veiculo'); 

    html = '<div class="row mt-4">\
            <div class="col-sm-6 mb-4"> <input name="modelo" type="text" class="form-control" placeholder="Modelo..."> </div>\
            <div class="col-sm-6"> <input name="marca" type="text" class="form-control" placeholder="Marca..."></div>\
            <div class="col-sm-6 mb-4"><input name="ano" min="1900" max="2050" type="number" class="form-control" placeholder="Ano..."></div>\
            <div class="col-sm-6"><input name="placa" maxlength="9" type="text" class="form-control" placeholder="Placa..."></div>\
            <div class="col-sm-6 mb-4"><label class="file" for="upload-img">Adicione uma imagem</label><input id="upload-img" name="imagem" type="file" class="form-control-file"></div>\
            <div class="col-sm-6 mb-4">\
                <button type="button" class="btn btn-danger mt-1" onclick="this.parentElement.parentElement.remove()">Excluir</button>\
            </div>\
            <hr> </div>'
    container.innerHTML += html
}

function exibir_form(n){
    att = document.getElementById('form_att')
    add = document.getElementById('form_add')

    if(n == 1){
        form = document.querySelector('#form-att-veiculos')
        form.innerHTML = '' 
        add.style.display = 'block'
        att.style.display = 'none'
    }
    else if(n == 2){
        att.reset()
        form = document.querySelector('#form_att_cliente')
        form.style.display = 'none' 
        add.style.display = 'none'
        att.style.display = 'block'
        form = document.querySelector('#form-att-veiculos')
        form.innerHTML = '' 
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

        console.log(data)

        for(let i=0; i < data['veiculos'].length; i++) {
  
            div_veiculo.innerHTML += '<div>\
            <div class="row">\
                <div class="col-sm-6">\
                    <input value="'+ data['veiculos'][i]['veiculo']['modelo'] +'" name="modelo" type="text" class="form-control" placeholder="Modelo..."> \
                </div>\
                <div class="col-sm-6">\
                <input value="'+ data['veiculos'][i]['veiculo']['marca'] +'" name="marca" type="text" class="form-control" placeholder="Marca...">\
                </div>\
            </div>\
            <div class="row mt-3 mb-3">\
                <div class="col-sm-6">\
                <input value="'+ data['veiculos'][i]['veiculo']['ano'] +'" name="ano" min="1900" max="2050" type="number" class="form-control" placeholder="Ano...">\
                </div>\
                <div class="col-sm-3">\
                <input value="'+ data['veiculos'][i]['veiculo']['placa'] +'" name="placa" maxlength="9" type="text" class="form-control" placeholder="Placa...">\
                </div>\
                <div class="col-sm-3 d-flex justify-content-center">\
                    <button type="button" data-id="'+ data['veiculos'][i]['id']+'" id="rm-car" class="btn btn-danger rm">Excluir</button>\
                    </div>\
                    \
                    </div><hr></div>\
                    <input type="hidden" name="car_id" value="'+ data['veiculos'][i]['id']+'"></input>\
                    \
                    '
                        
                    }
                    rmCar = document.querySelectorAll('.rm');
                    arrayRmCar = Array.from(rmCar);
    
                    for (let j = 0; j < arrayRmCar.length; j++) {
                        arrayRmCar[j].addEventListener('click', function(e) {
                            id = String(e.target.dataset.id)
                            inputHidden = document.createElement('input');
                            inputHidden.type = 'hidden';
                            inputHidden.value = id;
                            inputHidden.name = 'rm_car';

                            parentElement = e.target.parentElement.parentElement.parentElement.parentElement;
                            parentElement.appendChild(inputHidden);
                            e.target.parentElement.parentElement.parentElement.remove();
                        });
                    }

    })
}

