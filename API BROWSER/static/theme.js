const toggleBtn = document.getElementById('theme-toggle');
const body = document.body;

// Load saved theme from localStorage
if (localStorage.getItem('theme') === 'dark') {
  body.classList.add('dark');
  toggleBtn.textContent = '☀️';
}

// Toggle theme on click
toggleBtn.addEventListener('click', () => {
  body.classList.toggle('dark');
  const isDark = body.classList.contains('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  toggleBtn.textContent = isDark ? '☀️' : '🌙';
});
