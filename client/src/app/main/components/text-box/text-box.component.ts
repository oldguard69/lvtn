import { CdkVirtualScrollViewport } from '@angular/cdk/scrolling';
import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  Input,
  ViewChild,
} from '@angular/core';
import { Store } from '@ngrx/store';
import {
  SuspiciousStatItem,
  HighligthObject,
} from '../../interface/susp-stat.interface';
import { selectSourceSentences } from '../../state/selectors';

@Component({
  selector: 'app-text-box',
  templateUrl: './text-box.component.html',
  styleUrls: ['./text-box.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TextBoxComponent implements OnInit {
  @Input() sentences!: string[];
  @Input() fileType: 'susp' | 'src' = 'susp';
  @Input() fileStat!: SuspiciousStatItem[];
  @Input() srcFileName!: string | null;
  highlight!: HighligthObject[];

  @ViewChild('cdkViewport') cdkViewport!: CdkVirtualScrollViewport;
  constructor(private store: Store) {}

  ngOnInit(): void {
    this.initializeHighLight()
  }

  ngOnChanges(): void {
    this.initializeHighLight()
  }

  ngAfterViewInit() {
    this.scrollToTop();
  }

  initializeHighLight() {
    if (this.fileType === 'src') {
      this.highlight = this.fileStat
        .filter((item) => item.srcFile === this.srcFileName)
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
      this.store.select(selectSourceSentences).subscribe(res =>
        this.cdkViewport.scrollToIndex(0, 'smooth')
      )
    }
  }
}
