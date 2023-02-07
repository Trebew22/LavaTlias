# Lavatlias
LavaTlias é uma aplicação web local para gerenciamento de serviços automotivos. Com ele, você pode registrar clientes, veículos e realizar pedidos de serviço, sejam eles para lavagem ou análise por um mecânico. O projeto foi desenvolvido a base de Django, CSS, HTML e SQlite.

# Funcionalidades
<ul>
  <li>Cadastro de clientes</li>
  <li>Cadastro de veículos</li>
  <li>Gerenciamento de pedidos de serviço</li>
  <li>Emissão de relatórios em PDF com informações sobre os pedidos</li>
  <li>Envio de templates de e-mails para o cliente no console</li>
  <li>Entre outras funcionalidades.</li>
</ul>

# Requisitos
Para executar esse projeto, você precisa ter o Docker instalado em sua máquina.

# Instalação
Clone ou faça o download desse repositório
Abra o terminal e vá até a pasta do projeto
Execute o comando "docker-compose up --build"
Acesse a aplicação através do endereço http://localhost:8000 no seu navegador.

# Observações
Certifique-se de que todas as dependências descritas no arquivo Pipfile estejam instaladas antes de executar o projeto. Além disso, verifique as configurações de banco de dados no arquivo settings.py e, se necessário, altere-as de acordo com as suas necessidades.
