btn_procurar = document.getElementById('procurar')
input_url = document.getElementById('input_url')
resolution = document.getElementsByName('resolution')
format = document.getElementsByName('format')
btn_procurar.addEventListener('click',()=>{
    let url = input_url.value

    if (document.getElementsByName('resolution')[0].checked){
        var qualidade = 'hight'}
    else{
        var qualidade = 'lower'}

    if (document.getElementsByName('format')[0].checked){
        var formato = 'mp4'}
    else{
        var formato = 'mp3'}
        
    window.location = `${window.location.origin}/download?url=${url}&resolution=${qualidade}&format=${formato}`
})