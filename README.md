# ClimaCloset

## Development Setup with GitHub Codespaces

1. **Create a Codespace**:
   - Click the **Code** button on the repository page.
   - Select **Codespaces** and click **Create codespace on main**.

2. **Wait for the Codespace to initialize**:
   - This will set up the development container automatically using the configurations in `.devcontainer/devcontainer.json`.

3. **Set the `API_KEY` environment variable**:
   - In your Codespace, go to **Settings** > **Codespaces Secrets**.
   - Add a new secret named `API_KEY` with your API key.

4. **Run the Flask app**:
   - Open a terminal in the Codespace.
   - Run the application:

     ```bash
     flask run --host=0.0.0.0
     ```

5. **Access the app**:
   - Forward port **5000** when prompted.
   - Open the forwarded port in your browser to view the app.
