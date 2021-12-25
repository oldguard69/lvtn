export interface SuspiciousDoc {
    id: number,
    num_of_sentences: number,
    num_of_plg_sentences: number,
    is_plg: boolean,
    filename: string,
    unique_filename: string,
    user_id: number,
    num_of_plg_paragraphs: number
}