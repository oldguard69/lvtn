import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { Store } from '@ngrx/store';
import {
  HighligthObject,
  SuspiciousStatItem,
} from '../../interface/susp-stat.interface';
import { selectSourceSentences } from '../../state/selectors';

@Component({
  selector: 'app-raw-scroll',
  templateUrl: './raw-scroll.component.html',
  styleUrls: ['./raw-scroll.component.scss'],
})
export class RawScrollComponent implements OnInit {
  @Input() sentences!: string[];
  @Input() fileType: 'susp' | 'src' = 'susp';
  @Input() fileStat!: SuspiciousStatItem[];
  @Input() srcFileName!: string | null;
  highlight!: HighligthObject[];
  constructor(private store: Store) {}
  @ViewChild('itemsviewport') viewport!: ElementRef;

  ngOnInit(): void {
    this.initializeHighLight();
  }

  ngOnChanges(): void {
    this.initializeHighLight();
  }

  ngAfterViewInit() {
    this.scrollToTop();
  }

  initializeHighLight() {
    if (this.fileType === 'src') {
      this.highlight = this.fileStat
        .filter((item) => item.src_file === this.srcFileName)
        .map((item) => ({
          indexRange: item.srcIndexRange,
          colorClass: item.colorClass,
        }));
    } else {
      this.highlight = this.fileStat.map((item) => ({
        indexRange: item.suspIndexRange,
        colorClass: item.colorClass,
      }));
    }
  }

  getClassColor(i: number): string {
    for (let index = 0; index < this.highlight.length; index++) {
      if (this.highlight[index].indexRange.has(i)) {
        return this.highlight[index].colorClass;
      }
    }
    return 'no-color';
  }

  private scrollToTop() {
    if (this.fileType == 'src') {
      this.store.select(selectSourceSentences).subscribe((res) => {
        // console.log(this.viewport)
        this.viewport.nativeElement.scrollTop = 0;
      });
    }
  }
}
