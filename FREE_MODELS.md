# Free Models in OpenCode

All models with **$0 input / $0 output** cost.

---

## Quick Switch Commands

Run inside OpenCode chat:

```bash
# General purpose
/model opencode/longcat-2.5-preview-free
/model opencode/space-bunny-free

# Fast responses
/model opencode/mimo-v2.6-flash-free
/model opencode/nemotron-3.5-lightning-free

# Creative tasks
/model opencode/muse-spark-1.3-contributor-free

# Finance/analysis
/model opencode/ling-3.0-flash-fin-free
```

---

## Model Details

| Model | ID | Variants | Best For |
|-------|-----|----------|----------|
| **LongCat 2.5 Preview Free** | `opencode/longcat-2.5-preview-free` | None | General purpose |
| **Space Bunny Free** | `opencode/space-bunny-free` | low, medium, high, xhigh, max | General purpose (configurable depth) |
| **MiMo-V2.6-Flash Free** | `opencode/mimo-v2.6-flash-free` | None | Fast responses |
| **Muse Spark 1.3 Free** | `opencode/muse-spark-1.3-contributor-free` | minimal, low, medium, high, xhigh | Creative tasks |
| **Ling 3.0 Flash Fin Free** | `opencode/ling-3.0-flash-fin-free` | None | Finance/analysis |
| **Nemotron 3.5 Lightning Free** | `opencode/nemotron-3.5-lightning-free` | None | Fast, efficient |

---

## Set as Default in `opencode.json`

```json
{
  "model": "opencode/space-bunny-free",
  "mcp": { ... }
}
```

Replace the model ID with any from above.

---

## Notes

- **Variants** (low/medium/high/xhigh/max) control reasoning depth — set via `/model opencode/space-bunny-free:high`
- All models are hosted by OpenCode — no API keys needed
- Sessions are independent; model choice doesn't persist across sessions unless set in config