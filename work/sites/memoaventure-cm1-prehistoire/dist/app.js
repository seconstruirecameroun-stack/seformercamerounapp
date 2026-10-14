const state = JSON.parse(localStorage.getItem('memoaventure-progress') || '{}');
state.lesson = Boolean(state.lesson);
state.games = Array.isArray(state.games) ? state.games : [];
state.quiz = Boolean(state.quiz);
state.quizScore = Number(state.quizScore || 0);

const questions = [
  {
    text: 'Quel événement marque la fin de la Préhistoire ?',
    options: ['La découverte du feu', 'L’invention de l’écriture', 'Le début de la chasse', 'La fabrication des bijoux'],
    answer: 1,
    explain: 'L’invention de l’écriture, vers 3 000 avant J.-C., marque la fin de la Préhistoire.'
  },
  {
    text: 'Comment appelle-t-on l’âge de la pierre taillée ?',
    options: ['Le Paléolithique', 'Le Néolithique', 'L’âge du bronze', 'L’Antiquité'],
    answer: 0,
    explain: 'Le Paléolithique correspond à l’âge de la pierre taillée.'
  },
  {
    text: 'Quelles activités sont associées au Paléolithique dans la leçon ?',
    options: ['Écriture et commerce', 'Chasse, pêche et cueillette', 'Agriculture uniquement', 'Fabrication de bijoux en bronze'],
    answer: 1,
    explain: 'Les humains du Paléolithique vivent notamment de la chasse, de la pêche et de la cueillette.'
  },
  {
    text: 'À quelle période commence-t-on à pratiquer l’agriculture ?',
    options: ['Au Paléolithique', 'À l’âge des métaux', 'Au Néolithique', 'Après l’invention de l’écriture'],
    answer: 2,
    explain: 'Dans cette leçon, l’agriculture apparaît avec le Néolithique, l’âge de la pierre polie.'
  },
  {
    text: 'Que fabrique-t-on pendant l’âge des métaux ?',
    options: ['Seulement des maisons', 'Des outils et des bijoux', 'Des livres', 'Des outils en plastique'],
    answer: 1,
    explain: 'Le cours indique que les humains fabriquent des outils et des bijoux en métal.'
  }
];

let currentQuestion = 0;
let quizScore = 0;
let quizAnswers = [];
let speech = null;

function saveState() {
  localStorage.setItem('memoaventure-progress', JSON.stringify(state));
  renderProgress();
}

function routeTo(route) {
  document.querySelectorAll('.view').forEach(view => view.classList.toggle('active', view.id === route));
  document.querySelectorAll('[data-route]').forEach(button => button.classList.toggle('active', button.dataset.route === route && (button.classList.contains('nav-item') || button.closest('.mobile-nav'))));
  const target = document.getElementById(route);
  document.getElementById('page-title').textContent = target?.dataset.title || 'MémoAventure';
  history.replaceState(null, '', `#${route}`);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.querySelectorAll('[data-route]').forEach(el => el.addEventListener('click', event => {
  event.preventDefault();
  routeTo(el.dataset.route);
}));

document.querySelectorAll('[data-scroll-target]').forEach(el => el.addEventListener('click', () => {
  const targetId = el.dataset.scrollTarget;
  setTimeout(() => document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 120);
}));

function renderProgress() {
  const reviewDone = state.quiz;
  const completed = Number(state.lesson) + Number(state.games.length === 3) + Number(state.quiz) + Number(reviewDone);
  document.getElementById('home-progress-label').textContent = `${completed} sur 4 terminée${completed > 1 ? 's' : ''}`;
  document.getElementById('home-progress-bar').style.width = `${completed * 25}%`;
  setStatus('status-lesson', state.lesson, 'À faire');
  setStatus('status-games', state.games.length === 3, state.lesson ? 'Prêt' : 'À faire');
  setStatus('status-quiz', state.quiz, state.games.length === 3 ? 'Prêt' : 'À faire');
  const review = document.getElementById('status-review');
  review.textContent = state.quiz ? (state.quizScore === 5 ? 'Parfait' : 'À revoir') : 'Bloqué';
  review.classList.toggle('done', state.quiz);
  document.getElementById('game-score').textContent = state.games.length;
  state.games.forEach(index => restoreGame(index));
}

function setStatus(id, done, fallback) {
  const el = document.getElementById(id);
  el.textContent = done ? 'Terminé ✓' : fallback;
  el.classList.toggle('done', done);
}

function toast(message) {
  const el = document.getElementById('toast');
  el.textContent = message;
  el.classList.add('show');
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.remove('show'), 2800);
}

function speak(text) {
  if (!('speechSynthesis' in window)) {
    toast('La lecture audio n’est pas disponible sur ce navigateur.');
    return;
  }
  window.speechSynthesis.cancel();
  speech = new SpeechSynthesisUtterance(text);
  speech.lang = 'fr-FR';
  speech.rate = .88;
  window.speechSynthesis.speak(speech);
}

document.getElementById('listen-lesson').addEventListener('click', () => speak(
  'La Préhistoire commence avec l’apparition des premiers humains et se termine avec l’invention de l’écriture, vers trois mille avant Jésus Christ. Au Paléolithique, les humains taillent la pierre et vivent de la chasse, de la pêche et de la cueillette. Au Néolithique, ils polissent la pierre et commencent à pratiquer l’agriculture. Pendant l’âge des métaux, ils fabriquent des outils et des bijoux en métal.'
));

document.getElementById('lesson-done').addEventListener('click', () => {
  state.lesson = true;
  saveState();
  toast('Premier fragment gagné ! Place aux jeux.');
  setTimeout(() => routeTo('jeux'), 700);
});

document.querySelectorAll('.game-card').forEach(card => {
  card.querySelectorAll('.choice-stack button').forEach(button => button.addEventListener('click', () => answerGame(card, button)));
});

function answerGame(card, button) {
  const feedback = card.querySelector('.feedback');
  const index = Number(card.dataset.game);
  card.querySelectorAll('button').forEach(btn => btn.classList.remove('wrong'));
  if (button.dataset.correct === 'true') {
    button.classList.add('correct');
    card.classList.add('solved');
    card.querySelectorAll('.choice-stack button').forEach(btn => btn.disabled = true);
    feedback.textContent = ['Exact ! Le Paléolithique est la première période étudiée.', 'Bravo ! L’agriculture est associée au Néolithique.', 'Oui ! L’écriture marque la fin de la Préhistoire.'][index];
    if (!state.games.includes(index)) state.games.push(index);
    saveState();
    if (state.games.length === 3) toast('Les trois défis sont gagnés !');
  } else {
    button.classList.add('wrong');
    feedback.textContent = 'Pas encore. Regarde la frise et essaie une autre réponse.';
  }
}

function restoreGame(index) {
  const card = document.querySelector(`.game-card[data-game="${index}"]`);
  if (!card || card.classList.contains('solved')) return;
  const correct = card.querySelector('[data-correct="true"]');
  correct.classList.add('correct');
  card.classList.add('solved');
  card.querySelectorAll('.choice-stack button').forEach(btn => btn.disabled = true);
  card.querySelector('.feedback').textContent = 'Défi déjà gagné ✓';
}

document.getElementById('start-quiz').addEventListener('click', startQuiz);
document.getElementById('retry-quiz').addEventListener('click', startQuiz);
document.getElementById('next-question').addEventListener('click', () => {
  currentQuestion += 1;
  if (currentQuestion < questions.length) renderQuestion(); else showResult();
});
document.getElementById('read-question').addEventListener('click', () => {
  if (document.getElementById('quiz-question').classList.contains('active')) speak(questions[currentQuestion].text);
  else speak('Interrogation sur la Préhistoire. Cinq questions, sans piège.');
});

function startQuiz() {
  currentQuestion = 0;
  quizScore = 0;
  quizAnswers = [];
  switchQuizPanel('quiz-question');
  renderQuestion();
}

function switchQuizPanel(id) {
  document.querySelectorAll('.quiz-panel').forEach(panel => panel.classList.toggle('active', panel.id === id));
}

function renderQuestion() {
  const question = questions[currentQuestion];
  document.getElementById('question-count').textContent = `QUESTION ${currentQuestion + 1} SUR ${questions.length}`;
  document.getElementById('question-text').textContent = question.text;
  document.getElementById('quiz-progress-bar').style.width = `${(currentQuestion / questions.length) * 100}%`;
  document.getElementById('quiz-feedback').textContent = '';
  document.getElementById('next-question').classList.add('hidden');
  const options = document.getElementById('quiz-options');
  options.innerHTML = '';
  question.options.forEach((option, index) => {
    const button = document.createElement('button');
    button.textContent = option;
    button.addEventListener('click', () => selectQuizAnswer(index));
    options.appendChild(button);
  });
}

function selectQuizAnswer(index) {
  const question = questions[currentQuestion];
  const buttons = [...document.querySelectorAll('#quiz-options button')];
  buttons.forEach(button => button.disabled = true);
  buttons[question.answer].classList.add('correct');
  const correct = index === question.answer;
  if (!correct) buttons[index].classList.add('wrong'); else quizScore += 1;
  quizAnswers.push({ correct, question: question.text, explain: question.explain });
  const feedback = document.getElementById('quiz-feedback');
  feedback.textContent = `${correct ? 'Bravo ! ' : 'À retenir : '}${question.explain}`;
  feedback.style.color = correct ? '#3f7548' : '#984733';
  const next = document.getElementById('next-question');
  next.textContent = currentQuestion === questions.length - 1 ? 'Voir mon résultat →' : 'Question suivante →';
  next.classList.remove('hidden');
  document.getElementById('quiz-progress-bar').style.width = `${((currentQuestion + 1) / questions.length) * 100}%`;
}

function showResult() {
  switchQuizPanel('quiz-result');
  state.quiz = true;
  state.quizScore = quizScore;
  saveState();
  document.getElementById('result-title').textContent = quizScore === 5 ? 'Explorateur expert !' : quizScore >= 3 ? 'Très belle mission !' : 'Tu es sur le bon chemin !';
  document.getElementById('result-score').textContent = `Tu as obtenu ${quizScore} bonne${quizScore > 1 ? 's' : ''} réponse${quizScore > 1 ? 's' : ''} sur 5.`;
  const review = document.getElementById('result-review');
  review.innerHTML = quizAnswers.map(item => `<div class="review-line ${item.correct ? 'ok' : 'no'}"><span>${item.correct ? '✓' : '→'}</span><div><strong>${item.correct ? 'Acquis' : 'À revoir'}</strong><br>${item.explain}</div></div>`).join('');
  toast('Résultat enregistré dans ce navigateur.');
}

document.getElementById('edit-transcript').addEventListener('click', () => {
  const display = document.getElementById('transcript-display');
  const editor = document.getElementById('transcript-editor');
  const button = document.getElementById('edit-transcript');
  const editing = editor.classList.contains('hidden');
  display.classList.toggle('hidden', editing);
  editor.classList.toggle('hidden', !editing);
  button.textContent = editing ? 'Enregistrer' : 'Modifier';
  if (!editing) toast('Transcription enregistrée localement.');
});

document.getElementById('approve-correction').addEventListener('click', event => {
  event.currentTarget.closest('.alert-card').innerHTML = '<span class="alert-icon" style="background:#6f9a76">✓</span><div><p class="eyebrow dark">POINT VALIDÉ</p><h3>La maîtrise du feu sera présentée au Paléolithique</h3><p>La correction parent sera utilisée dans la prochaine fiche.</p></div>';
  toast('Correction validée par le parent.');
});
document.getElementById('keep-source').addEventListener('click', () => toast('Le contenu du cahier est conservé tel quel.'));
document.getElementById('upload-button').addEventListener('click', () => document.getElementById('course-upload').click());
document.getElementById('course-upload').addEventListener('change', event => {
  const count = event.target.files.length;
  document.getElementById('upload-status').textContent = count ? `${count} fichier${count > 1 ? 's' : ''} prêt${count > 1 ? 's' : ''} à être analysé${count > 1 ? 's' : ''}.` : '';
});

renderProgress();
const initialRoute = location.hash.slice(1);
routeTo(document.getElementById(initialRoute) ? initialRoute : 'accueil');
