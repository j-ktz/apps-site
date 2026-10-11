/* Sitout sit-out board.
 *
 * A port of the sit-out rule in Sitout's pairing engine (ByeLedger.chooseSitOuts):
 * the player with the fewest sit-outs sits next; on a tie, whoever sat longest ago;
 * then roster order. Courts hold four players each and the rest sit.
 * Sit-outs only: the app also rotates partners and opponents, which this demo skips.
 * Checked against the Swift engine for 4–24 players x 1–6 courts x 12 rounds.
 */
(function (root) {
  "use strict";

  function sitOutSchedule(players, courts, rounds) {
    var courtsUsed = Math.max(0, Math.min(courts, Math.floor(players / 4)));
    var playing = courtsUsed * 4;
    var sitting = players - playing;
    var byes = [], last = [], order = [], i, r;
    for (i = 0; i < players; i++) { byes.push(0); last.push(-1); order.push(i); }
    var out = [];
    for (r = 1; r <= rounds; r++) {
      var chosen = [];
      if (sitting > 0) {
        var ranked = order.slice().sort(function (a, b) {
          if (byes[a] !== byes[b]) return byes[a] - byes[b];
          if (last[a] !== last[b]) return last[a] - last[b];
          return a - b;
        });
        chosen = ranked.slice(0, sitting).sort(function (a, b) { return a - b; });
        for (i = 0; i < chosen.length; i++) { byes[chosen[i]] += 1; last[chosen[i]] = r; }
      }
      out.push(chosen);
    }
    return { courtsUsed: courtsUsed, playing: playing, sitting: sitting, rounds: out, byes: byes };
  }

  /* Rounds until everyone has sat out at least once (0 when nobody sits). */
  function firstCycle(players, courts) {
    var s = sitOutSchedule(players, courts, 0).sitting;
    return s > 0 ? Math.ceil(players / s) : 0;
  }

  if (typeof module === "object" && module.exports) {
    module.exports = { sitOutSchedule: sitOutSchedule, firstCycle: firstCycle };
    return;
  }

  var doc = root.document;
  var board = doc.getElementById("board");
  if (!board) return;

  var ROUNDS = 12;
  var state = { players: 9, courts: 2 };
  var limits = { players: [4, 24], courts: [1, 6] };

  try {
    var q = new URLSearchParams(root.location.search);
    ["players", "courts"].forEach(function (k) {
      var v = parseInt(q.get(k), 10);
      if (v >= limits[k][0] && v <= limits[k][1]) state[k] = v;
    });
  } catch (e) { /* keep defaults */ }

  var reduce = root.matchMedia && root.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function plural(n, one, many) { return n + " " + (n === 1 ? one : many); }
  function list(names) {
    if (names.length <= 1) return names.join("");
    return names.slice(0, -1).join(", ") + " and " + names[names.length - 1];
  }

  function render() {
    var n = state.players, c = state.courts;
    var s = sitOutSchedule(n, c, ROUNDS);

    doc.getElementById("players-v").textContent = n;
    doc.getElementById("courts-v").textContent = c;
    doc.querySelectorAll(".stepper").forEach(function (st) {
      var k = st.getAttribute("data-key");
      st.querySelector(".dec").disabled = state[k] <= limits[k][0];
      st.querySelector(".inc").disabled = state[k] >= limits[k][1];
    });

    var readout;
    var sits = s.sitting + (s.sitting === 1 ? " sits" : " sit") + " out each round.";
    if (s.courtsUsed < c) {
      readout = n + " players can fill only " + plural(s.courtsUsed, "court", "courts") + ": " +
        s.playing + " play" + (s.sitting === 0 ? " and nobody sits out." : " and " + sits);
    } else if (s.sitting === 0) {
      readout = n + " players fill " + plural(c, "court", "courts") + " exactly. Nobody sits out.";
    } else {
      readout = n + " players on " + plural(c, "court", "courts") + ": " + s.playing + " play and " + sits;
    }
    doc.getElementById("readout").textContent = readout;

    var lo = Math.min.apply(null, s.byes), hi = Math.max.apply(null, s.byes);
    var check;
    if (s.sitting === 0) {
      check = "With nobody sitting, there is nothing to balance.";
    } else {
      var cycle = firstCycle(n, c);
      var first = cycle <= ROUNDS
        ? "Everyone has sat out once by round " + cycle + ". "
        : "Everyone gets a first sit-out by round " + cycle + ". ";
      check = first + "After " + ROUNDS + " rounds, " + (lo === hi
        ? "every player has sat out " + plural(lo, "time", "times") + "."
        : "each player has sat out " + lo + " or " + hi + " times, never more than one apart.");
    }
    doc.getElementById("check").textContent = check;

    // The visual board (hidden from screen readers; the list below carries the same facts).
    board.style.setProperty("--n", n);
    board.classList.toggle("compact", n > 12);
    var html = '<span class="corner">Round</span>';
    for (var p = 1; p <= n; p++) html += '<span class="ph' + (p > 9 ? " w" : "") + '"><span class="pp">P</span>' + p + "</span>";
    s.rounds.forEach(function (sit, r) {
      var set = {};
      sit.forEach(function (i) { set[i] = true; });
      html += '<span class="rh" style="--d:' + r + '">' + (r + 1) + "</span>";
      for (var i = 0; i < n; i++) {
        html += set[i] ? '<i class="c sit" style="--d:' + r + '"></i>' : '<i class="c" style="--d:' + r + '"></i>';
      }
    });
    html += '<span class="rh tot">Sat</span>';
    s.byes.forEach(function (b) { html += '<span class="tv' + (b > 9 ? " w" : "") + '">' + b + "</span>"; });
    board.innerHTML = html;
    if (reduce) board.classList.add("still");

    var items = s.rounds.map(function (sit, r) {
      var label = "Round " + (r + 1) + ": ";
      if (sit.length === 0) return "<li>" + label + "everyone plays.</li>";
      if (sit.length <= s.playing) {
        return "<li>" + label + list(sit.map(function (i) { return "P" + (i + 1); })) +
          (sit.length === 1 ? " sits out." : " sit out.") + "</li>";
      }
      var on = [];
      for (var i = 0; i < n; i++) if (sit.indexOf(i) < 0) on.push("P" + (i + 1));
      return "<li>" + label + list(on) + " play; everyone else sits out.</li>";
    });
    doc.getElementById("board-text").innerHTML = items.join("");
  }

  doc.querySelectorAll(".stepper").forEach(function (st) {
    var k = st.getAttribute("data-key");
    st.querySelector(".dec").addEventListener("click", function () {
      if (state[k] > limits[k][0]) { state[k] -= 1; render(); }
    });
    st.querySelector(".inc").addEventListener("click", function () {
      if (state[k] < limits[k][1]) { state[k] += 1; render(); }
    });
  });

  render();
})(this);
