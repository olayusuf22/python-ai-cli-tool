# BONUS: CLI for Kubernetes Diagnostics

## 💡 Idea
This CLI can help diagnose Kubernetes cluster issues using AI-powered analysis.
It can interpret `kubectl` outputs, logs, and manifest files to provide insights.

## 🧰 Example Command
```bash
python cli.py run llama3 "Analyze this Kubernetes error: CrashLoopBackOff on nginx pod"
```

**Output:**
```
The 'CrashLoopBackOff' means the container is repeatedly failing.
Common causes include incorrect startup commands or missing dependencies.
Try checking logs with `kubectl logs <pod>` or verifying your image locally.
```

## 🔮 Future Enhancements
- Integrate with `kubectl` to fetch logs automatically.
- Add `--file` flag to analyze YAML manifests.
- Suggest Helm chart or resource configuration improvements.


=== requirements.txt ===

argparse
