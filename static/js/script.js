document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".card .slider").forEach((slider) => {
    const before = slider.querySelector(".before");
    const after = slider.querySelector(".after");
    const btnPrev = slider.querySelector(".prev");
    const btnNext = slider.querySelector(".next");

    btnPrev.addEventListener("click", () => {
      before.style.opacity = "1";
      after.style.opacity = "0";
    });
    btnNext.addEventListener("click", () => {
      before.style.opacity = "0";
      after.style.opacity = "1";
    });
  });
});
document.querySelectorAll('.slider').forEach(slider => {
  const beforeImg = slider.querySelector('img.before');
  const afterImg = slider.querySelector('img.after');
  const btnPrev = slider.querySelector('button.prev');
  const btnNext = slider.querySelector('button.next');

  // Começa mostrando a imagem "antes"
  let showingBefore = true;

  function showBefore() {
    beforeImg.style.opacity = '1';
    afterImg.style.opacity = '0';
    showingBefore = true;
  }

  function showAfter() {
    beforeImg.style.opacity = '0';
    afterImg.style.opacity = '1';
    showingBefore = false;
  }

  btnPrev.addEventListener('click', () => {
    showBefore();
  });

  btnNext.addEventListener('click', () => {
    showAfter();
  });

  // Inicia mostrando o antes
  showBefore();
});

function revealOnScroll() {
  const reveals = document.querySelectorAll('.reveal');
  const windowHeight = window.innerHeight;
  const revealPoint = 100;

  reveals.forEach(element => {
    const elementTop = element.getBoundingClientRect().top;
    if (elementTop < windowHeight - revealPoint) {
      element.classList.add('active');
    } else {
      element.classList.remove('active');
    }
  });
}

window.addEventListener('scroll', revealOnScroll);
window.addEventListener('load', revealOnScroll); // para ativar ao carregar
