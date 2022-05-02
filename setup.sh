mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"innocentmunai@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "[theme]
primaryColor='#a5c489'
backgroundColor='#46484a'
secondaryBackgroundColor='#3A8FB7'
textColor='#e1e5eb'
font='sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml