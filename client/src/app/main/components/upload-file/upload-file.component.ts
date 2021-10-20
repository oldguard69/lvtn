import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.scss'],
})
export class UploadFileComponent implements OnInit {
  fileToUpload!: File;
  isLoading: boolean = false;
  constructor(private apiService: ApiService, private router: Router) {}

  ngOnInit(): void {}

  handleFileInput(target: any) {
    const file = target.files.item(0);
    this.fileToUpload = file as File;
    // console.log(target.files)
  }

  uploadFile() {
    this.isLoading = true;
    this.apiService.uploadFile(this.fileToUpload).subscribe(
      (data: any) => {
        console.log('File has been upload');
        this.isLoading = false;
        this.router.navigateByUrl(`/main/suspicious-docs/${data['id']}`);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  confirmExit(): boolean {
    if (this.isLoading) {
      if (confirm('Do you wish to Please confirm')) {
        return true;
      } else {
        return false;
      }
    } else {
      return true;
    }
  }
}
