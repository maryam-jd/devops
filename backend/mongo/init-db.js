db = db.getSiblingDB('tododb');
db.createCollection('todos');
db.todos.insertMany([
  { title: 'Complete DevOps Lab Final', description: 'Submit Docker, K8s, CI/CD, and Selenium tasks', completed: false, priority: 'high', createdAt: new Date() },
  { title: 'Push Docker images to Docker Hub', description: 'Build and push frontend and backend images', completed: false, priority: 'high', createdAt: new Date() },
  { title: 'Deploy to Azure Kubernetes Service', description: 'Create AKS cluster and deploy all 3 pods', completed: false, priority: 'medium', createdAt: new Date() },
  { title: 'Set up GitHub Actions CI/CD', description: 'Pipeline with build, test, and push stages', completed: false, priority: 'medium', createdAt: new Date() },
  { title: 'Run Selenium Test Suite', description: 'Execute all 3 automated test cases and screenshot results', completed: false, priority: 'low', createdAt: new Date() }
]);
print('✅ Database initialized with sample todos');