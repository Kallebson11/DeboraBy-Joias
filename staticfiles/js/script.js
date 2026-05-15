document.addEventListener('DOMContentLoaded', function () {

    // ============================================================
    // CARROSSEL DE CATEGORIAS
    // ============================================================
    const categoryList = document.querySelector('.category-list');
    const prevBtn      = document.querySelector('.prev-btn');
    const nextBtn      = document.querySelector('.next-btn');

    if (categoryList && prevBtn && nextBtn) {
        const itemWidth = 112;
        prevBtn.addEventListener('click', () => categoryList.scrollBy({ left: -itemWidth * 3, behavior: 'smooth' }));
        nextBtn.addEventListener('click', () => categoryList.scrollBy({ left:  itemWidth * 3, behavior: 'smooth' }));
    }

    // ============================================================
    // CARROSSEL COMPLETE O LOOK
    // ============================================================
    const lookList    = document.getElementById('completeLookList');
    const lookPrevBtn = document.querySelector('.look-prev-btn');
    const lookNextBtn = document.querySelector('.look-next-btn');

    if (lookList && lookPrevBtn && lookNextBtn) {
        const step = 280 * 2;
        lookPrevBtn.addEventListener('click', () => lookList.scrollBy({ left: -step, behavior: 'smooth' }));
        lookNextBtn.addEventListener('click', () => lookList.scrollBy({ left:  step, behavior: 'smooth' }));
    }

    // ============================================================
    // BOTÕES +/- DE QUANTIDADE
    // ============================================================
    document.querySelectorAll('.btn-quantity-plus').forEach(btn => {
        btn.addEventListener('click', function () {
            const inp = this.parentElement.querySelector('.quantity-input');
            if (inp && parseInt(inp.value) < 10) inp.value = parseInt(inp.value) + 1;
        });
    });
    document.querySelectorAll('.btn-quantity-minus').forEach(btn => {
        btn.addEventListener('click', function () {
            const inp = this.parentElement.querySelector('.quantity-input');
            if (inp && parseInt(inp.value) > 1) inp.value = parseInt(inp.value) - 1;
        });
    });

    // ============================================================
    // BOTÕES DE TAMANHO (detalhe do produto)
    // ============================================================
    document.querySelectorAll('.detail-size-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.detail-size-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            const val = this.dataset.size;
            const label = document.getElementById('size-selected');
            const hidden = document.getElementById('tamanho-selecionado');
            if (label)  label.textContent = val;
            if (hidden) hidden.value = val;
        });
    });

    // ============================================================
    // VALIDAÇÃO DE SENHA — REGISTRO
    // ============================================================
    const regPassInput    = document.getElementById('id_password1');
    const regConfirmInput = document.getElementById('id_password2');
    const regFeedback     = document.getElementById('confirm-feedback');
    const regForm         = document.getElementById('register-form');
    const regInlineError  = document.getElementById('inline-error');

    if (regForm) {
        const regRules = buildPasswordRules();

        if (regPassInput)    regPassInput.addEventListener('input',    () => runPasswordValidation(regPassInput, regConfirmInput, regFeedback, regRules));
        if (regConfirmInput) regConfirmInput.addEventListener('input', () => runConfirmValidation(regPassInput, regConfirmInput, regFeedback));

        regForm.addEventListener('submit', function (e) {
            const pass    = regPassInput    ? regPassInput.value    : '';
            const confirm = regConfirmInput ? regConfirmInput.value : '';
            resetPasswordState(regRules, regFeedback, regInlineError);
            if (!passwordIsValid(pass) || pass !== confirm) {
                e.preventDefault();
                if (regInlineError) regInlineError.style.display = 'block';
            } else {
                sessionStorage.setItem('register_success', '1');
            }
        });
    }

    // ============================================================
    // VALIDAÇÃO DE SENHA — RECOVER
    // ============================================================
    const recPassInput    = document.getElementById('id_new_password');
    const recConfirmInput = document.getElementById('id_confirm_password');
    const recFeedback     = document.getElementById('confirm-feedback');
    const recForm         = document.getElementById('recover-form');
    const recInlineError  = document.getElementById('inline-error');

    if (recForm) {
        const recRules = buildPasswordRules();

        if (recPassInput)    recPassInput.addEventListener('input',    () => runPasswordValidation(recPassInput, recConfirmInput, recFeedback, recRules));
        if (recConfirmInput) recConfirmInput.addEventListener('input', () => runConfirmValidation(recPassInput, recConfirmInput, recFeedback));

        recForm.addEventListener('submit', function (e) {
            const pass    = recPassInput    ? recPassInput.value    : '';
            const confirm = recConfirmInput ? recConfirmInput.value : '';
            resetPasswordState(recRules, recFeedback, recInlineError);
            if (!passwordIsValid(pass) || pass !== confirm) {
                e.preventDefault();
                if (recInlineError) recInlineError.style.display = 'block';
            } else {
                sessionStorage.setItem('recover_success', '1');
            }
        });
    }

    // ============================================================
    // SESSIONstorage — ALERTAS DE SUCESSO
    // ============================================================
    if (sessionStorage.getItem('register_success')) {
        sessionStorage.removeItem('register_success');
        alert('Registro realizado com sucesso!');
    }
    if (sessionStorage.getItem('recover_success')) {
        sessionStorage.removeItem('recover_success');
        alert('Senha atualizada com sucesso!');
    }

});

// ============================================================
// ACCORDION DE DESCRIÇÃO (detalhe do produto)
// Precisa ser global pois é chamado via onclick="" no HTML
// ============================================================
function toggleAccordion(bodyId, btnId) {
    const body = document.getElementById(bodyId);
    const btn  = document.getElementById(btnId);
    if (!body || !btn) return;
    const icon = btn.querySelector('.detail-accordion-icon');
    icon.textContent = body.classList.toggle('open') ? '−' : '+';
}

// ============================================================
// HELPERS DE VALIDAÇÃO DE SENHA (usados por register e recover)
// ============================================================
function buildPasswordRules() {
    return [
        { el: document.getElementById('rule-length'),       check: p => p.length > 0 && p.length < 8 },
        { el: document.getElementById('rule-uppercase'),    check: p => p.length > 0 && !/[A-Z]/.test(p) },
        { el: document.getElementById('rule-lowercase'),    check: p => p.length > 0 && !/[a-z]/.test(p) },
        { el: document.getElementById('rule-numeric-only'), check: p => p.length > 0 && /^\d+$/.test(p) },
        { el: document.getElementById('rule-special'),      check: p => p.length > 0 && !/[!@#$%^&*()\-_=+\[\]{}|;:,.<>?]/.test(p) },
        { el: document.getElementById('rule-space'),        check: p => p.includes(' ') },
    ].filter(r => r.el !== null); // ignora regras sem elemento no DOM
}

function runPasswordValidation(passInput, confirmInput, feedback, rules) {
    if (!passInput) return;
    const val = passInput.value;
    rules.forEach(({ el, check }) => el.classList.toggle('violated', check(val)));
    if (confirmInput && confirmInput.value.length > 0)
        runConfirmValidation(passInput, confirmInput, feedback);
}

function runConfirmValidation(passInput, confirmInput, feedback) {
    if (!confirmInput || !passInput || !feedback) return;
    if (confirmInput.value.length === 0) {
        feedback.className = 'confirm-msg';
        feedback.innerHTML = '';
        return;
    }
    const match = passInput.value === confirmInput.value;
    feedback.className = match ? 'confirm-msg success' : 'confirm-msg error';
    feedback.innerHTML = match
        ? '<span>✓</span> Senhas coincidem'
        : '<span>✕</span> As senhas não coincidem';
}

function resetPasswordState(rules, feedback, inlineError) {
    if (rules)       rules.forEach(({ el }) => el.classList.remove('violated'));
    if (feedback)    { feedback.className = 'confirm-msg'; feedback.innerHTML = ''; }
    if (inlineError) inlineError.style.display = 'none';
}

function passwordIsValid(p) {
    return (
        p.length >= 8 &&
        /[A-Z]/.test(p) &&
        /[a-z]/.test(p) &&
        !/^\d+$/.test(p) &&
        /[!@#$%^&*()\-_=+\[\]{}|;:,.<>?]/.test(p) &&
        !p.includes(' ')
    );
}