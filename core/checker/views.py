from django.shortcuts import render
from .models import ProjectAbstract
from sentence_transformers import SentenceTransformer, util
import torch

# Load the AI model into memory (this downloads a ~80MB model the first time it runs)
# all-MiniLM-L6-v2 is specifically trained to map sentences & paragraphs to a 384 dimensional dense vector space to understand meaning.
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_idea_similarity(text1, text2):
    """Compares the underlying meaning/idea of two texts."""
    if not text1 or not text2:
        return 0.0
    
    # Convert texts into mathematical "idea vectors"
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)
    
    # Calculate how close the two ideas are using Cosine Similarity
    similarity = util.cos_sim(embedding1, embedding2).item()
    
    # Ensure the score stays between 0 and 100
    return max(0, min(100, round(similarity * 100, 2)))

def checker_home(request):
    context = {}

    if request.method == 'POST':
        new_abstract = request.POST.get('abstract', '').strip()
        
        if new_abstract:
            saved_projects = ProjectAbstract.objects.all()
            highest_sim = 0.0
            best_match_text = "Database is empty. You are the first submission!"

            # Compare the NEW idea against EVERY saved idea
            if saved_projects.exists():
                for project in saved_projects:
                    sim_score = calculate_idea_similarity(new_abstract, project.content)
                    if sim_score > highest_sim:
                        highest_sim = sim_score
                        best_match_text = project.content
            
            # Save the newly submitted abstract to the database
            ProjectAbstract.objects.create(content=new_abstract)

            context['similarity_score'] = highest_sim
            context['best_match'] = best_match_text
            context['submitted_text'] = new_abstract
            
            # Because AI understands paraphrasing, semantic scores run higher. 
            # We adjust the thresholds to reflect "Idea match" vs "Word match".
            if highest_sim > 80:
                context['risk_level'] = 'High Risk - Same Idea/Output'
                context['color_theme'] = '#ff4757' 
            elif highest_sim > 55:
                context['risk_level'] = 'Moderate Risk - Shared Concepts'
                context['color_theme'] = '#ffa502' 
            else:
                context['risk_level'] = 'Low Risk - Unique Idea'
                context['color_theme'] = '#2ed573' 

    return render(request, 'checker/index.html', context)