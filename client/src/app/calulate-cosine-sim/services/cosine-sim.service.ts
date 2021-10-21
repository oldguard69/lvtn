import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface CalculateCosineSimBody {
  sent1: string;
  sent2: string;
  perform_cleaning: boolean;
}

export interface CalculateCosineSimResult {
  cosine_similarity: number;
  is_plagiarism: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class CosineSimService {
  constructor(
    private http: HttpClient,
    @Inject('API_URL') private api_url: string
  ) {}

  calculateCosineSimilarity(
    body: CalculateCosineSimBody
  ): Observable<CalculateCosineSimResult> {
    return this.http
      .post(`${this.api_url}/calulcate-cosine-similarity`, body)
      .pipe(map((res: any) => res['result']));
  }
}
