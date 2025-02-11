const gameOverPopup = document.getElementById("gameOverPopup");
const gameResult = document.getElementById("gameResult");
const restartButton = document.getElementById("restartButton");

export function showGameOver(winner, paddle1, paddle2) {
  gameResult.innerHTML =
    winner === true
      ? `You Win!<br><div style="display: inline-block; padding: 10px; background-color:rgb(0, 255, 0); border-radius: 5px; font-size: 20px;">${paddle1} : ${paddle2}</div>`
      : `You Lose!<br><div style="display: inline-block; padding: 10px; background-color:rgb(255, 0, 0); border-radius: 5px; font-size: 20px;">${paddle1} : ${paddle2}</div>`;
  gameOverPopup.style.display = "flex";
}

// 나가는 기능은 미구현임
restartButton.addEventListener("click", function () {
  gameOverPopup.style.display = "none";
});
