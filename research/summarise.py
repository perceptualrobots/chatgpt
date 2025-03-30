
from research.article import ArticleQuery

if __name__ == "__main__":
    # Example usage
    summarizer = ArticleQuery()

    article_paths = [
        # "G:/My Drive/newideas/2024.12.06.627286v2.full.pdf"

    #   "G:/My Drive/newideas/PIIS0092867419306403.pdf",
    #     "G:/My Drive/newideas/PIIS0896627322006699.pdf",
    #     "G:/My Drive/newideas/elife-04811-v1.pdf",
    #     "G:/My Drive/newideas/NIPS-2011-a-reinforcement-learning-theory-for-homeostatic-regulation-Paper.pdf",
    #     "G:/My Drive/newideas/ijcnn2023-all.pdf",
    #     "G:/My Drive/newideas/1-s2.0-S0896627322011254-main.pdf",
    #     "G:/My Drive/newideas/2f1e2daa976863dcb94c903a5455e5cf.pdf",
    #     "G:/My Drive/newideas/s41467-020-17828-8.pdf",
        "G:/My Drive/newideas/2024.12.06.627286v2.full.pdf"
    #     "G:/My Drive/newideas/nihms99493.pdf",
    #     "G:/My Drive/newideas/Roseboom_Arnold_2011_Reaching_Invisible.pdf",
    #     "G:/My Drive/newideas/PIIS0960982213001401.pdf",
    #     "G:/My Drive/newideas/whyte2020.pdf",
    #     "G:/My Drive/newideas/2410.06633v1.pdf",
    #     "G:/My Drive/newideas/1-s2.0-S2665945X22000092-main.pdf"


    ]
    output_doc = "/tmp/summaries.docx"
    summarizer.process_articles(article_paths, output_doc)
    print(f"Summaries saved to {output_doc}")