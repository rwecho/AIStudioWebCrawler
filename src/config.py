from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DEFAULT_DETAIL_SYS_PROMPT = """You are the good SEO Editor. Now you should write the new_content based on the template_content, the new_content should output with markdown format. The first level of markdown should be h3. When outputting, do not start with the sentence "Here is the content" . The content of the new_content  have modules including what, feature, how, price, helpful tips, Frequently Asked Questions. And you should get the keyword of the content, and generate the content about the keyword as more as you can. The markdown title level of these modules is h3. Direct output\n. The base content_template is\n: What is tap4.ai?\n tap4.ai is an AI-driven platform that provides access to a vast array of AI technologies for various needs, including ChatGPT, GPT-4o for text generation and image understanding, Dalle3 for image creation for document analysis\n. What is the main feature of tap4.ai? \n 1.Collect more than 1000 AIs and 200+ categories;\n 2. Discover the AI tools easily; 3. Free ai tools submission;\n  How to use tap4.ai?\n Every user can utilize GPT-4o for free up to 20 times a day on tap4.ai. Subscribing to the platform grants additional benefits and extended access beyond the free usage limits.\n Can I generate images using tap4.ai?\n Yes, with Dalle3's text-to-image generation capability, users can create images, sharing credits with GPT-4o for a seamless creative experience.\n How many GPTs are available on tap4.ai?\n tap4.ai offers nearly 200,000 GPT models for a wide variety of applications in work, study, and everyday life. You can freely use these GPTs without the need for a ChatGPT Plus subscription.\n How can I maximize my use of tap4.ai's AI services?\n By leveraging the daily free uses of GPT-4o document reading, and Dalle's image generation, users can explore a vast range of AI-powered tools to support various tasks.\n Will my information be used for your training data?\n We highly value user privacy, and your data will not be used for any training purposes. If needed, you can delete your account at any time, and all your data will be removed as well.\n When would I need a tap4.ai subscription?\n If the 20 free GPT-4o conversations per day do not meet your needs and you heavily rely on GPT-4o, we invite you to subscribe to our affordable products. Just output the markdown content!"""
DEFAULT_TAG_SELECTOR_SYS_PROMPT = """According to the content. Select several suitable tags from the tag_list list, tags cannot be created, tags can only be selected from tag_list. Just output selected tags!"""
DEFAULT_LANGUAGE_SYS_PROMPT = """translate into {language}(all sentences), keep original format(such as the input is markdown, output is also markdown), easy understand. Not need output note!"""


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")  # Default value if not set
    GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "5000"))

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    DETAIL_SYS_PROMPT = os.getenv("DETAIL_SYS_PROMPT", DEFAULT_DETAIL_SYS_PROMPT)
    TAG_SELECTOR_SYS_PROMPT = os.getenv(
        "TAG_SELECTOR_SYS_PROMPT", DEFAULT_TAG_SELECTOR_SYS_PROMPT
    )
    LANGUAGE_SYS_PROMPT = os.getenv("LANGUAGE_SYS_PROMPT", DEFAULT_LANGUAGE_SYS_PROMPT)


config = Config()
