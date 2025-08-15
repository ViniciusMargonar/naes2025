from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re


# Crie uma classe de formulário para o cadastro de usuários
# A herança é feita para poder tornar o email único e obrigatório
# E outros campos, se necessário
class UsuarioCadastroForm(UserCreationForm):

    email = forms.EmailField(required=True, help_text="Informe um email válido.")
    
    # Redefinindo o campo username para adicionar validações personalizadas
    username = forms.CharField(
        max_length=150,
        min_length=8,
        help_text="Mínimo de 8 letras. Apenas letras são permitidas, sem números ou caracteres especiais."
    )
    
    # Redefinindo o campo password1 para adicionar texto de ajuda personalizado
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        help_text="• Sua senha precisa conter pelo menos 8 caracteres.<br>• Sua senha não pode ser inteiramente numérica.<br>• Sua senha precisa pelo menos uma letra"
    )

    # Define o model e os fields que vão aparecer na tela
    class Meta:
        model = User
        # Esses dois passwords são para verificar se as senhas são iguais
        fields = ['username', 'email', 'password1', 'password2']

    # Validação personalizada para o nome de usuário
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Verifica se tem pelo menos 8 caracteres
        if len(username) < 8:
            raise forms.ValidationError("O nome de usuário deve ter pelo menos 8 caracteres.")
        
        # Verifica se contém apenas letras (sem números ou caracteres especiais)
        if not username.isalpha():
            raise forms.ValidationError("O nome de usuário deve conter apenas letras, sem números ou caracteres especiais.")
        
        # Verifica se já existe um usuário com este nome
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        
        return username

    # Validação personalizada para a senha
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        # Verifica se tem pelo menos 8 caracteres
        if len(password1) < 8:
            raise forms.ValidationError("Sua senha precisa conter pelo menos 8 caracteres.")
        
        # Verifica se é inteiramente numérica
        if password1.isdigit():
            raise forms.ValidationError("Sua senha não pode ser inteiramente numérica.")
        
        # Verifica se contém pelo menos uma letra
        if not re.search(r'[a-zA-Z]', password1):
            raise forms.ValidationError("Sua senha precisa conter pelo menos uma letra.")
        
        return password1

    # O metodo clean no forms serve de validação para os campos
    def clean_email(self):
        # recebe o email do formulário
        email = self.cleaned_data.get('email')
        # Verifica se já existe algum usuário com este email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email
