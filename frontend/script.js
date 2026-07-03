const gamesList = document.querySelector("#gamesList");
const gameSelect = document.querySelector("#gameSelect");
const membersList = document.querySelector("#membersList");
const registerForm = document.querySelector("#registerForm");
const teamNameInput = document.querySelector("#teamName");
const addMemberButton = document.querySelector("#addMemberButton");
const message = document.querySelector("#message");
const teamsTable = document.querySelector("#teamsTable");

const gameLogos = {
  RoV: {
    src: "/assets/rov-logo.png",
    alt: "RoV Arena of Valor logo",
  },
  Valorant: {
    src: "/assets/valorant-logo.svg",
    alt: "Valorant logo",
  },
  "FC Online": {
    src: "/assets/fc-online-logo.svg",
    alt: "EA Sports FC Online logo",
  },
};

function updateSelectedGameCard(selectedGame) {
  document.querySelectorAll(".game-card").forEach((card) => {
    const isSelected = card.dataset.game === selectedGame;
    card.classList.toggle("is-selected", isSelected);
    card.setAttribute("aria-pressed", String(isSelected));
  });
}

function selectGame(game) {
  gameSelect.value = game;
  gameSelect.dispatchEvent(new Event("change", { bubbles: true }));
  document.querySelector(".form-panel").scrollIntoView({ behavior: "smooth", block: "start" });
  teamNameInput.focus({ preventScroll: true });
}

function setMessage(text, type) {
  message.textContent = text;
  message.className = `message ${type || ""}`.trim();
}

function createMemberInput(value = "") {
  const row = document.createElement("div");
  row.className = "member-row";

  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "ชื่อสมาชิก";
  input.value = value;
  input.className = "member-input";

  const removeButton = document.createElement("button");
  removeButton.type = "button";
  removeButton.className = "icon-button";
  removeButton.title = "ลบสมาชิก";
  removeButton.textContent = "×";
  removeButton.addEventListener("click", () => {
    if (document.querySelectorAll(".member-input").length > 3) {
      row.remove();
    } else {
      input.value = "";
      input.focus();
    }
  });

  row.append(input, removeButton);
  membersList.append(row);
}

function resetMemberInputs() {
  membersList.innerHTML = "";
  for (let index = 0; index < 3; index += 1) {
    createMemberInput();
  }
}

async function loadGames() {
  const response = await fetch("/games");
  const data = await response.json();

  gamesList.innerHTML = "";
  gameSelect.innerHTML = "";

  data.games.forEach((game) => {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "game-card";
    button.dataset.game = game;
    button.setAttribute("aria-label", `เลือกเกม ${game} แล้วไปหน้าลงทะเบียน`);
    button.setAttribute("aria-pressed", "false");
    button.addEventListener("click", () => selectGame(game));

    const logo = gameLogos[game];
    const logoWrap = document.createElement("div");
    logoWrap.className = "game-logo-wrap";

    if (logo) {
      const image = document.createElement("img");
      image.src = logo.src;
      image.alt = logo.alt;
      image.width = 180;
      image.height = 84;
      image.loading = "eager";
      logoWrap.append(image);
    } else {
      logoWrap.textContent = game;
    }

    const name = document.createElement("span");
    name.className = "sr-only";
    name.textContent = game;

    button.append(logoWrap, name);
    item.append(button);
    gamesList.append(item);

    const option = document.createElement("option");
    option.value = game;
    option.textContent = game;
    gameSelect.append(option);
  });

  updateSelectedGameCard(gameSelect.value);
}

async function loadTeams() {
  const response = await fetch("/teams");
  const data = await response.json();

  teamsTable.innerHTML = "";

  if (data.teams.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 3;
    cell.className = "empty-state";
    cell.textContent = "ยังไม่มีทีมที่ลงทะเบียน";
    row.append(cell);
    teamsTable.append(row);
    return;
  }

  data.teams.forEach((team) => {
    const row = document.createElement("tr");
    const teamCell = document.createElement("td");
    const gameCell = document.createElement("td");
    const membersCell = document.createElement("td");

    teamCell.textContent = team.team_name;
    gameCell.textContent = team.game;
    membersCell.textContent = team.members.join(", ");

    row.append(teamCell, gameCell, membersCell);
    teamsTable.append(row);
  });
}

addMemberButton.addEventListener("click", () => createMemberInput());
gameSelect.addEventListener("change", () => updateSelectedGameCard(gameSelect.value));

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setMessage("", "");

  const members = [...document.querySelectorAll(".member-input")]
    .map((input) => input.value.trim())
    .filter(Boolean);

  const payload = {
    team_name: teamNameInput.value.trim(),
    game: gameSelect.value,
    members,
  };

  const response = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const result = await response.json();

  if (result.success) {
    setMessage(result.message, "success");
    registerForm.reset();
    resetMemberInputs();
    await loadTeams();
  } else {
    setMessage(result.message, "error");
  }
});

async function init() {
  resetMemberInputs();
  try {
    await loadGames();
    await loadTeams();
  } catch (error) {
    setMessage("โหลดข้อมูลไม่สำเร็จ กรุณาตรวจสอบ Backend", "error");
  }
}

init();
