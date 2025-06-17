import streamlit as st
import google.generativeai as genai

api_key = st.secrets("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

def calcular_tmb(sexo: str, idade: int, peso: float, altura: float) -> float:
    sexo = sexo.lower()
    if sexo == 'masculino':
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
    elif sexo == 'feminino':
        tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)
    else:
        raise ValueError("Sexo inválido. Use 'masculino' ou 'feminino'.")
    return tmb

def gerar_resposta_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# Configuração da página
st.set_page_config(page_title="Fitness.AI", page_icon="🚀")

# Título da aplicação
st.title("Seja bem-vindo ao Fitness.AI! 🚀")

st.write("Seu personal trainer e nutricionista virtual, sempre pronto para ajudar você a alcançar seus objetivos de fitness!")

nome = st.text_input("Digite seu nome:")
idade = st.number_input("Idade:", min_value=0, max_value=120)
sexo = st.selectbox("Sexo:", ["feminino", "masculino"])
biotipo = st.selectbox("Biotipo:", ["ectomorfo", "mesomorfo", "endomorfo"])
st.write("Lembre-se: Ectomorfo = tendência a emagrecer, Mesomorfo = tendência atlética, Endomorfo = tendência a engordar.")
altura = st.number_input("Altura (cm):", 100, 250, 170)
peso = st.number_input("Peso (kg):", value=70)


tmb = calcular_tmb(sexo, idade, peso, altura)
txmb = st.number_input("Taxa metabólica basal (TMB):", min_value=500, max_value=10000, value=int(tmb))
st.write("TMB é a energia mínima para manter funções vitais em repouso. não alterar caso não saiba o valor exato.")

# Nível de atividade física
atividade_dict = {
    1: ("Sedentário", 1.2),
    2: ("Levemente ativo", 1.375),
    3: ("Moderadamente ativo", 1.55),
    4: ("Muito ativo", 1.725),
    5: ("Extremamente ativo", 1.9)
}
st.write("Nível de atividade física:")
atividade = st.slider("Nível de atividade:", 1, 5, 1)
fator_atividade = atividade_dict[atividade][1]
st.write(f"Selecionado: {atividade_dict[atividade][0]}")
st.write("1 - Sedentário: praticamente não faz nada | 2 - Levemente ativo: exercícios leves 1-3x/semana | 3 - Moderadamente ativo: exercícios moderados 3-5x/semana | 4 - Muito ativo: exercícios pesados 6-7x/semana | 5 - Extremamente ativo: exercícios muito pesados, duas vezes ao dia.")

tdee = int(txmb * fator_atividade)
st.write(f"Seu TDEE estimado é: {tdee} calorias por dia.")

# Quantas vezes por semana deseja ir para a academia
frequencia_academia = st.slider("Quantas vezes por semana você quer ir para a academia?", 1, 7, 3)

# Alimentos que não gosta/não pode comer
alimentos_nao_gosta = st.text_area("Alimentos que você NÃO gosta ou NÃO pode comer (separe por vírgula):")

# Alimentos que gosta e fazem parte do seu cotidiano
alimentos_gosta = st.text_area("Alimentos que você GOSTA e fazem parte do seu cotidiano (separe por vírgula):")

objetivo = st.selectbox("Qual seu objetivo?", ["emagrecer", "emagrecer rápido", "manter", "ganhar massa muscular", "ganhar massa muscular rápido"])
atual = st.selectbox("Qual seu estado atual?", ["magreza", "massa muscular considerável", "falso magro", "acima do peso", "obesidade leve", "obesidade moderada", "obesidade severa"])

if st.button("Gerar treino e dieta personalizada"):
    with st.spinner("Gerando plano personalizado..."):
        prompt = f"""
        Meu nome é {nome}, tenho {idade} anos, sou do sexo {sexo}, biotipo {biotipo}, altura {altura} cm, peso {peso} kg. Minha TMB é {txmb} e meu TDEE é {tdee}. Meu objetivo é {objetivo} e meu estado atual é {atual}.
        Quero ir para a academia {frequencia_academia} vezes por semana.
        Não gosto/não posso comer: {alimentos_nao_gosta}.
        Gosto e costumo comer: {alimentos_gosta}.
        Gere um plano de treino semanal e uma sugestão de dieta diária personalizada para mim, considerando todas essas informações, restrições e preferências alimentares. Seja detalhado, prático e objetivo.
        """
        resposta = gerar_resposta_gemini(prompt)
        st.subheader("Plano de Treino e Dieta Personalizada:")
        st.write(resposta)


