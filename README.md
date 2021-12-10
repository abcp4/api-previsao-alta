# Previsão de Óbito

Uma Api para previsão de risco de óbito ou melhora. É possível acessar a documentação da API em:  https://ml-paciente.herokuapp.com/docs

## Como executar?

Para o funcionamento desta api é necessário possui o python instalado e as seguintes bibliotecas:
- fastapi
- scikit-learn
- uvicorn
- imbalanced-learn

Após instalar as dependências, para executar a API em modo de desenvolvimento execute o seguinte comando:

```python
    uvicorn main:app --reload
```

A documentação da API ficará disponível por padrão no endereço http://127.0.0.1:8000/docs
