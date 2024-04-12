<script>
  import { onMount } from "svelte";
  import "xterm/css/xterm.css";
  import { agentState } from "$lib/store";

  let terminalElement;
  let terminal;
  let fitAddon;
  // agentState.subscribe((value) => {
  //   $agentState = value;
  // });

  onMount(async () => {
    let xterm = await import("xterm");
    let xtermAddonFit = await import("xterm-addon-fit");

    terminal = new xterm.Terminal({
      disableStdin: true,
      cursorBlink: true,
      convertEol: true,
      rows: 1,
      theme: {
        background: "#d3d3d3",
        foreground: "#000000",
        innerText: "#000000",
        cursor: "#000000",
      },
    });
    fitAddon = new xtermAddonFit.FitAddon();
    terminal.loadAddon(fitAddon);
    terminal.open(terminalElement);
    fitAddon.fit();

    agentState.subscribe((states) => {
      console.log("agentState states", states);

      if (states && states.terminal_session && states.terminal_session.command) {
        terminal.reset();
        const { command, output, title } = states.terminal_session;
        addCommandAndOutput(command, output, title);
      }

      // Find the last state with a non-null terminal_session
      // const lastStateWithTerminalSession = states
      //   .slice()
      //   .reverse()
      //   .find(
      //     (state) => state.terminal_session && state.terminal_session.command
      //   );

      // if (lastStateWithTerminalSession) {
      //   const { command, output, title } =
      //     lastStateWithTerminalSession.terminal_session;
      //   addCommandAndOutput(command, output, title);
      // } else {
      //   terminal.write("Waiting...\r\n");
      // }

      fitAddon.fit();
    });
  });

  function addCommandAndOutput(command, output, title) {
    terminal.write(`\x1b[2J\x1b[0;0H`); // Clear the terminal
    if (title) {
      terminal.write(`${title}\r\n`);
      // document.getElementById("terminal-title").innerText = title;
    }
    // terminal.reset();
    terminal.write(`$ ${command}\r\n\r\n${output}\r\n`);
  }
</script>

<div class="flex flex-col border-2 rounded-lg h-1/2">
  <div class="p-2 flex items-center border-b">
    <div class="flex space-x-2 ml-2 mr-4">
      <div class="w-3 h-3 bg-red-500 rounded-full"></div>
      <div class="w-3 h-3 bg-yellow-400 rounded-full"></div>
      <div class="w-3 h-3 bg-green-500 rounded-full"></div>
    </div>
    <span id="terminal-title">Terminal</span>
  </div>
  <div
    id="terminal-content"
    class="h-full w-full rounded-bl-lg"
    bind:this={terminalElement}
  ></div>
</div>

<style>
  #terminal-content :global(.xterm) {
    padding: 10px;
    height: 100%; /* Ensure terminal content height is fixed */
  }

  #terminal-content :global(.xterm-viewport) {
    overflow-y: auto !important;
    height: 100%;
  }
</style>
