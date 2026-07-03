const totalTeams = document.querySelector("#totalTeams");
const totalMembers = document.querySelector("#totalMembers");
const totalGames = document.querySelector("#totalGames");
const barChart = document.querySelector("#barChart");
const donutChart = document.querySelector("#donutChart");
const donutLegend = document.querySelector("#donutLegend");
const latestTeamsTable = document.querySelector("#latestTeamsTable");
const dashboardMessage = document.querySelector("#dashboardMessage");
const refreshButton = document.querySelector("#refreshButton");

const chartColors = ["#0f9f8f", "#f59e0b", "#4f6fbd"];

function setDashboardMessage(text, type = "") {
  dashboardMessage.textContent = text;
  dashboardMessage.className = `message ${type}`.trim();
}

function renderMetrics(stats) {
  totalTeams.textContent = stats.total_teams;
  totalMembers.textContent = stats.total_members;
  totalGames.textContent = stats.total_games;
}

function renderBarChart(byGame) {
  const maxTeams = Math.max(...byGame.map((item) => item.teams), 1);
  barChart.innerHTML = "";

  byGame.forEach((item, index) => {
    const row = document.createElement("div");
    row.className = "bar-row";

    const label = document.createElement("span");
    label.className = "bar-label";
    label.textContent = item.game;

    const track = document.createElement("div");
    track.className = "bar-track";

    const fill = document.createElement("div");
    fill.className = "bar-fill";
    fill.style.width = `${(item.teams / maxTeams) * 100}%`;
    fill.style.background = chartColors[index % chartColors.length];
    track.append(fill);

    const value = document.createElement("span");
    value.className = "bar-value";
    value.textContent = item.teams;

    row.append(label, track, value);
    barChart.append(row);
  });
}

function createDonutSegment(value, total, offset, color) {
  const radius = 44;
  const circumference = 2 * Math.PI * radius;
  const segment = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  segment.setAttribute("class", "donut-segment");
  segment.setAttribute("cx", "60");
  segment.setAttribute("cy", "60");
  segment.setAttribute("r", String(radius));
  segment.setAttribute("stroke", color);
  segment.setAttribute("stroke-dasharray", `${(value / total) * circumference} ${circumference}`);
  segment.setAttribute("stroke-dashoffset", String(-offset * circumference));
  segment.setAttribute("transform", "rotate(-90 60 60)");
  return segment;
}

function renderDonutChart(byGame) {
  const total = byGame.reduce((sum, item) => sum + item.teams, 0);
  donutChart.innerHTML = "";
  donutLegend.innerHTML = "";

  const empty = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  empty.setAttribute("class", "donut-empty");
  empty.setAttribute("cx", "60");
  empty.setAttribute("cy", "60");
  empty.setAttribute("r", "44");
  donutChart.append(empty);

  let offset = 0;
  byGame.forEach((item, index) => {
    const color = chartColors[index % chartColors.length];

    if (total > 0 && item.teams > 0) {
      donutChart.append(createDonutSegment(item.teams, total, offset, color));
      offset += item.teams / total;
    }

    const row = document.createElement("div");
    row.className = "legend-row";

    const name = document.createElement("span");
    name.className = "legend-name";

    const swatch = document.createElement("span");
    swatch.className = "legend-swatch";
    swatch.style.background = color;

    const label = document.createElement("span");
    label.textContent = item.game;
    name.append(swatch, label);

    const value = document.createElement("span");
    value.textContent = total > 0 ? `${Math.round((item.teams / total) * 100)}%` : "0%";

    row.append(name, value);
    donutLegend.append(row);
  });
}

function renderLatestTeams(teams) {
  latestTeamsTable.innerHTML = "";

  if (teams.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 3;
    cell.className = "empty-state";
    cell.textContent = "ยังไม่มีทีมที่ลงทะเบียน";
    row.append(cell);
    latestTeamsTable.append(row);
    return;
  }

  teams.forEach((team) => {
    const row = document.createElement("tr");
    const teamCell = document.createElement("td");
    const gameCell = document.createElement("td");
    const membersCell = document.createElement("td");

    teamCell.textContent = team.team_name;
    gameCell.textContent = team.game;
    membersCell.textContent = team.members.join(", ");

    row.append(teamCell, gameCell, membersCell);
    latestTeamsTable.append(row);
  });
}

async function loadDashboard() {
  setDashboardMessage("", "");
  refreshButton.disabled = true;

  try {
    const response = await fetch("/stats");
    const stats = await response.json();

    renderMetrics(stats);
    renderBarChart(stats.by_game);
    renderDonutChart(stats.by_game);
    renderLatestTeams(stats.latest_teams);
  } catch (error) {
    setDashboardMessage("โหลด Dashboard ไม่สำเร็จ กรุณาตรวจสอบ Backend", "error");
  } finally {
    refreshButton.disabled = false;
  }
}

refreshButton.addEventListener("click", loadDashboard);
loadDashboard();
