#include "IDAStar.h"
#include "StateSpaceSearch/Node.h"
#include <stack>
#include <memory>

IDAStar::IDAStar(const Heuristic &heuristic)
    :   heuristic(heuristic) {}

int IDAStar::solve(const Board &board) const {
    int costLimit = heuristic.estimateCost(board);

    while (true) {
        if (costLimitedDFS(board, costLimit)) {
            return costLimit;
        }

        ++costLimit;
    }
}

bool IDAStar::costLimitedDFS(const Board &board, int costLimit) const {
    auto open = std::stack<std::shared_ptr<Node>>();
    auto initNode = std::make_shared<Node>(Board(board));
    open.push(initNode);

    while (!open.empty()) {
        auto node = open.top();
        open.pop();

        if (node->getBoard().isSolved()) {
            return true;
        }

        for (auto &child : node->getChildren()) {
            int estimatedCost = child->getCost() + heuristic.estimateCost(child->getBoard());
            if (estimatedCost <= costLimit) {
                open.push(child);
            }
        }
    }

    return false;
}
