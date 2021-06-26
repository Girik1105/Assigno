let setTheme = localStorage.getItem('theme')

let colorSwapper = document.querySelector('#change-theme');
let stylesheet = document.querySelector('#color-mode');
let darkMode = false;

if (setTheme == null) {
  changeStyle(stylesheet, 'light_mode.css')
} 
else if (setTheme == false){
  changeStyle(stylesheet, 'dark_mode.css')
}
else if (setTheme == false){
  changeStyle(stylesheet, 'light_mode.css')
}

localStorage.setItem('theme', darkMode)

function changeStyle(stylesheet, cssSheet) {
  stylesheet.href = `{% static '${cssSheet}' %}`
  darkMode = true;
}

colorSwapper.addEventListener('click', () => {
  console.log('Btn works');
  if (darkMode) {
    changeStyle(stylesheet, 'light_mode.css') 
  } else {
    changeStyle(stylesheet, 'dark_mode.css') 
  } 
})