export interface SuspiciousStatItem {
    srcFile: string;
    paragraphLength: number;
    srcIndex: number;
    suspIndex: number;
    colorClass: string;
    srcIndexRange: Set<number>;
    suspIndexRange: Set<number>;
}

export interface HighligthObject {
    indexRange: Set<number>;
    colorClass: string;
}

interface Test {
    [key: string]: SuspiciousStatItem
}