# ClimaCloset

## Development Setup with GitHub Codespaces

1. **Create a Codespace**:
   - Click the **Code** button on the repository page.
   - Select **Codespaces** and click **Create codespace on main**.
  
     **--OR--**

     [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/jcarney2024/climacloset)

2. **Wait for the Codespace to initialize**:
   - This will set up the development container automatically using the configurations in `.devcontainer/devcontainer.json`.

3. **Run the Flask app**:
   - Open a terminal in the Codespace.
   - Run the application:

     ```bash
     flask run --debug --host=0.0.0.0
     ```

4. **Access the app**:
   - Forward port **5000** when prompted.
   - Open the forwarded port in your browser to view the app.
  
5. **Choose a feature to work on**:
   - Choose a feature from the projects tab on GitHub
   - Make sure to move it to a different category so no one else works on it!

6. **Add a new branch**:
   - Don't forget that when developing a new feature, you should be working on a new branch
  
     ```bash
     git checkout -b <your-branch-name>
     ```

7. **Make thoughtful commits when making progress**:
   ```bash
   git commit -am "Your commit message here"
   ```

8. **Push your changes (yay!)**:
   ```bash
   git push origin <your-branch-name>
   ```
9. ***Make a Pull Request**:
   - On GitHub go to the pull requests tab
   - Choose the branch you've been working on
   - Add a title and description
   - Submit!
   - YAYYY

10. **Tests and Preview Version**:
   - When you submit a PR, tests are automatically ran, and you will be told if they pass.
   - A preview version via Heroku will also be generated. View it to make sure everything is working right!
   - Wait for collaboraters to approve your PR to merge branches!
