#!/usr/bin/env python
"""Interactive CLI demo for the hackathon project."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.config import get_settings
from src.core.logging import configure_logging, get_logger
from src.models.nim_client import ChatMessage, get_chat_client, get_embedding_client, get_rerank_client

console = Console()
logger = get_logger(__name__)

app = typer.Typer(
    name="nebius-nvidia-hackathon",
    help="Nebius x NVIDIA Global AI Hackathon 2026 - Demo CLI",
    add_completion=False,
)


def print_banner() -> None:
    """Print the hackathon banner."""
    banner = """
███╗   ███╗ █████╗ ██████╗ ███████╗██████╗ ███████╗██████╗ 
████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██╔══██╗
██╔████╔██║███████║██████╔╝█████╗  ██████╔╝█████╗  ██████╔╝
██║╚██╔╝██║██╔══██║██╔══██╗██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗
██║ ╚═╝ ██║██║  ██║██║  ██║███████╗██║  ██║███████╗██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

     Nebius x NVIDIA Global AI Hackathon 2026
          🚀 Building the Future of AI
"""
    console.print(Panel(banner, style="bold green", border_style="green"))


def print_info_table() -> None:
    """Print configuration info."""
    settings = get_settings()
    table = Table(title="Configuration", show_header=True, header_style="bold cyan")
    table.add_column("Setting", style="yellow")
    table.add_column("Value", style="white")

    table.add_row("Environment", settings.app.environment)
    table.add_row("Mock NIM", str(settings.mock_nim))
    table.add_row("NVIDIA Model", settings.nvidia.llm_model)
    table.add_row("Embedding Model", settings.nvidia.embedding_model)
    table.add_row("Rerank Model", settings.nvidia.rerank_model)
    table.add_row("TensorRT-LLM", str(settings.nvidia.tensorrt_enabled))
    table.add_row("Quantization", settings.nvidia.tensorrt_quantization)

    console.print(table)


@app.command()
def chat(
    message: Optional[str] = typer.Argument(None, help="Initial message (starts interactive if omitted)"),
    temperature: float = typer.Option(0.7, "--temp", "-t", help="Temperature (0-2)"),
    max_tokens: int = typer.Option(4096, "--max-tokens", "-m", help="Max tokens to generate"),
    stream: bool = typer.Option(False, "--stream", "-s", help="Stream response"),
    session_id: Optional[str] = typer.Option(None, "--session", help="Session ID for conversation"),
):
    """Chat with the NVIDIA NIM model."""
    configure_logging()
    print_banner()
    print_info_table()

    client = get_chat_client()

    async def run_chat():
        messages = []

        if message:
            # Single message mode
            messages.append(ChatMessage(role="user", content=message))
            await process_message(messages, temperature, max_tokens, stream)
        else:
            # Interactive mode
            console.print("\n[bold cyan]Interactive Chat Mode[/bold cyan]")
            console.print("Type 'exit', 'quit', or 'q' to quit\n")

            while True:
                try:
                    user_input = Prompt.ask("[bold green]You[/bold green]")
                    if user_input.lower() in ("exit", "quit", "q"):
                        console.print("[yellow]Goodbye![/yellow]")
                        break

                    messages.append(ChatMessage(role="user", content=user_input))
                    await process_message(messages, temperature, max_tokens, stream)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Goodbye![/yellow]")
                    break
                except EOFError:
                    break

    asyncio.run(run_chat())


async def process_message(
    messages: list[ChatMessage],
    temperature: float,
    max_tokens: int,
    stream: bool,
) -> None:
    """Process a chat message and display response."""
    client = get_chat_client()

    try:
        if stream:
            console.print("[bold blue]Assistant[/bold blue]: ", end="")
            full_response = ""
            async for chunk in client.chat_completion_stream(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            ):
                # Parse SSE chunk
                if chunk.startswith("data: "):
                    data = chunk[6:]
                    if data == "[DONE]":
                        break
                    import json
                    try:
                        chunk_data = json.loads(data)
                        if "choices" in chunk_data and chunk_data["choices"]:
                            delta = chunk_data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                console.print(content, end="", highlight=False)
                                full_response += content
                    except json.JSONDecodeError:
                        pass
            console.print()  # New line after streaming
            messages.append(ChatMessage(role="assistant", content=full_response))
        else:
            with console.status("[bold blue]Thinking...[/bold blue]", spinner="dots"):
                response = await client.chat_completion(
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

            assistant_msg = response.choices[0].message.content
            messages.append(ChatMessage(role="assistant", content=assistant_msg))

            # Display response
            console.print(Panel(
                Markdown(assistant_msg),
                title="[bold blue]Assistant[/bold blue]",
                border_style="blue",
                padding=(1, 2),
            ))

            # Show metrics
            if response.usage:
                metrics_table = Table(show_header=False, box=None)
                metrics_table.add_column("Metric", style="cyan")
                metrics_table.add_column("Value", style="white")
                metrics_table.add_row("Prompt Tokens", str(response.usage.get("prompt_tokens", 0)))
                metrics_table.add_row("Completion Tokens", str(response.usage.get("completion_tokens", 0)))
                metrics_table.add_row("Total Tokens", str(response.usage.get("total_tokens", 0)))
                console.print(metrics_table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        logger.error("chat_error", error=str(e))


@app.command()
def embed(
    text: str = typer.Argument(..., help="Text to embed"),
    model: Optional[str] = typer.Option(None, "--model", help="Embedding model override"),
):
    """Generate embeddings for text."""
    configure_logging()
    print_banner()

    client = get_embedding_client()

    async def run_embed():
        with console.status("[bold blue]Generating embedding...[/bold blue]"):
            embedding = await client.embed_single(text)

        console.print(f"[green]✓[/green] Generated embedding: {len(embedding)} dimensions")
        console.print(f"First 10 values: {embedding[:10]}")

    asyncio.run(run_embed())


@app.command()
def rerank(
    query: str = typer.Argument(..., help="Query to rerank against"),
    documents: list[str] = typer.Argument(..., help="Documents to rerank"),
    top_n: Optional[int] = typer.Option(None, "--top-n", help="Number of top results"),
):
    """Rerank documents by relevance to query."""
    configure_logging()
    print_banner()

    client = get_rerank_client()

    async def run_rerank():
        with console.status("[bold blue]Reranking documents...[/bold blue]"):
            response = await client.rerank(query=query, documents=documents, top_n=top_n)

        table = Table(title="Rerank Results", show_header=True)
        table.add_column("Rank", style="cyan", width=6)
        table.add_column("Score", style="green", width=10)
        table.add_column("Document", style="white")

        for i, result in enumerate(response.results):
            table.add_row(str(i + 1), f"{result.relevance_score:.4f}", result.document[:80] + "..." if len(result.document) > 80 else result.document)

        console.print(table)

    asyncio.run(rerank())


@app.command()
def health():
    """Check health of all services."""
    configure_logging()
    print_banner()

    client = get_chat_client()
    embed_client = get_embedding_client()
    rerank_client = get_rerank_client()

    async def run_health():
        with console.status("[bold blue]Checking services...[/bold blue]"):
            chat_healthy = await client.health_check()
            embed_healthy = await embed_client.health_check()
            rerank_healthy = await rerank_client.health_check()

        table = Table(title="Service Health", show_header=True)
        table.add_column("Service", style="cyan")
        table.add_column("Status", style="white")

        table.add_row("Chat (NIM)", "🟢 Healthy" if chat_healthy else "🔴 Unhealthy")
        table.add_row("Embeddings (NIM)", "🟢 Healthy" if embed_healthy else "🔴 Unhealthy")
        table.add_row("Rerank (NIM)", "🟢 Healthy" if rerank_healthy else "🔴 Unhealthy")

        console.print(table)

    asyncio.run(run_health())


@app.command()
def benchmark(
    prompts: int = typer.Option(10, "--prompts", "-n", help="Number of prompts"),
    concurrent: int = typer.Option(1, "--concurrent", "-c", help="Concurrent requests"),
    max_tokens: int = typer.Option(100, "--max-tokens", help="Max tokens per response"),
):
    """Run performance benchmark."""
    configure_logging()
    print_banner()

    client = get_chat_client()

    import time
    import statistics

    test_prompts = [
        "Explain quantum computing in simple terms.",
        "Write a Python function to calculate fibonacci numbers.",
        "What are the benefits of using TensorRT-LLM?",
        "Describe the architecture of a transformer model.",
        "How does speculative decoding work?",
    ] * (prompts // 5 + 1)
    test_prompts = test_prompts[:prompts]

    async def run_benchmark():
        console.print(f"[bold]Benchmarking[/bold]: {prompts} prompts, {concurrent} concurrent, {max_tokens} max tokens")

        latencies = []
        token_counts = []
        errors = 0

        async def single_request(prompt: str):
            nonlocal errors
            start = time.perf_counter()
            try:
                response = await client.chat_completion(
                    messages=[ChatMessage(role="user", content=prompt)],
                    max_tokens=max_tokens,
                )
                latency = (time.perf_counter() - start) * 1000
                latencies.append(latency)
                if response.usage:
                    token_counts.append(response.usage.get("completion_tokens", 0))
            except Exception as e:
                errors += 1
                logger.error("benchmark_error", error=str(e))

        if concurrent == 1:
            for prompt in test_prompts:
                await single_request(prompt)
        else:
            semaphore = asyncio.Semaphore(concurrent)

            async def limited_request(prompt):
                async with semaphore:
                    await single_request(prompt)

            await asyncio.gather(*[limited_request(p) for p in test_prompts])

        # Results
        console.print("\n[bold green]Benchmark Results[/bold green]")
        results_table = Table(show_header=True)
        results_table.add_column("Metric", style="cyan")
        results_table.add_column("Value", style="white")

        results_table.add_row("Total Requests", str(prompts))
        results_table.add_row("Successful", str(prompts - errors))
        results_table.add_row("Errors", str(errors))
        results_table.add_row("Concurrency", str(concurrent))

        if latencies:
            results_table.add_row("Avg Latency", f"{statistics.mean(latencies):.1f} ms")
            results_table.add_row("Median Latency", f"{statistics.median(latencies):.1f} ms")
            results_table.add_row("P95 Latency", f"{statistics.quantiles(latencies, n=20)[18]:.1f} ms")
            results_table.add_row("P99 Latency", f"{statistics.quantiles(latencies, n=100)[98]:.1f} ms")
            results_table.add_row("Min Latency", f"{min(latencies):.1f} ms")
            results_table.add_row("Max Latency", f"{max(latencies):.1f} ms")

        if token_counts:
            total_tokens = sum(token_counts)
            total_time = sum(latencies) / 1000
            results_table.add_row("Total Tokens", str(total_tokens))
            results_table.add_row("Tokens/Second", f"{total_tokens / total_time:.1f}" if total_time > 0 else "N/A")
            results_table.add_row("Avg Tokens/Request", f"{statistics.mean(token_counts):.1f}")

        console.print(results_table)

    asyncio.run(run_benchmark())


@app.command()
def version():
    """Show version info."""
    print_banner()
    console.print("[bold]Version:[/bold] 0.1.0")
    console.print("[bold]Hackathon:[/bold] Nebius x NVIDIA Global AI Hackathon 2026")
    console.print("[bold]Repository:[/bold] https://github.com/rishisf12/nebius-nvidia-hackathon-showcase")


if __name__ == "__main__":
    app()